import logging
import logging.config
import os
import tempfile

import yaml
from fastapi import FastAPI, HTTPException
from fastapi import Response
from fastapi import status

import gkgaas.limes.preconfigs.profiles as limesprofiles
import gkgaas.triplegeo.preconfigs.profiles as triplegeoprofiles
from gkgaas.exceptions import WrongExecutablePath, RunnerExecutionFailed, \
    ProtocolNotSupportedException
from gkgaas.fagi import LinksFormat
from gkgaas.fagi.preconfigs.profiles import slipo_default_ab_mode
from gkgaas.fagi.runner import FAGIRunner
from gkgaas.limes.runner import LIMESRunner
from gkgaas.model import ConversionDescription, KnowledgeGraphConversionInformation, \
    KnowledgeGraphInfo
from gkgaas.sparqlserver.fusekiwrapper import FusekiWrapper
from gkgaas.triplegeo.runner import TripleGeoRunner
from gkgaas.utils.paths import get_file_name_base, get_links_file_path
from gkgaas.utils.pidserviceclient import DummyPIDServiceClient

logging.config.fileConfig(os.getenv('LOGGING_FILE_CONFIG', './logging.conf'))
logger = logging.getLogger(__name__)

default_rdf_file_postfix = '.nt'
gkgaas_app = FastAPI()

try:
    with open(os.path.join(os.getcwd(), 'settings.yml')) as yaml_file:
        cfg = yaml.safe_load(yaml_file)
except FileNotFoundError:
    raise Exception(
        'No settings.yml file found. Please create one, e.g. by copying the '
        'provided settings.yml.template.')


@gkgaas_app.get('/triplegeo/profiles/list')
def list_triplegeo_profiles():
    return [pn for pn in triplegeoprofiles.name_to_profile]


# FIXME: Replace dummy PID service with actual one
pid_service = DummyPIDServiceClient()
pid_service.set_id_mappings({
    'topio.arc.topio_kg.file': '/tmp/topio_kg/gis_osm_places_free_1.nt',
    'topio.iais.my_dataset.file':
        '/tmp/topio_kg/corfu/get_pois_v02_corfu_2100.shp'
})


def _get_file(topio_id: str):
    local_id: str = pid_service.get_custom_id(topio_id)

    if local_id is None:
        raise FileNotFoundError()

    if not (local_id.startswith('file://') or local_id.startswith('/')):
        raise ProtocolNotSupportedException(f'Cannot open {local_id}')

    if local_id.startswith('file://'):
        local_id = local_id.replace('file://', '')

    # File is opened to probe whether we have the permission to do so. If not
    # this will cause a permission error which is caught by the caller.
    file = open(local_id)

    return file


def get_file_path(topio_id: str) -> str:
    try:
        file = _get_file(topio_id)
        file_path = file.name
        file.close()

    except ProtocolNotSupportedException as e:
        logger.error(e.msg)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.msg
        )

    except PermissionError:
        err_msg = \
            f'No permission to access input file {topio_id}'

        logger.error(err_msg)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=err_msg
        )

    except FileNotFoundError:
        err_msg = f'Input file {topio_id} not found'

        logger.error(err_msg)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=err_msg
        )

    except OSError as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return file_path


@gkgaas_app.post('/add_to_knowledge_graph', status_code=status.HTTP_201_CREATED)
def add_to_knowledge_graph(
        kg_conversion_information: KnowledgeGraphConversionInformation
) -> KnowledgeGraphInfo:

    working_dir = tempfile.mkdtemp()

    ############################################################################
    # Data conversion - TripleGeo
    #

    # set up TripleGeo...
    try:
        triplegeo_cfg = cfg['triplegeo']
        triplegeo_exec_path = triplegeo_cfg['executable_path']
        triplegeo_profile_name = \
            kg_conversion_information.conversion_profile_name.lower()
        triplegeo_profile = \
            triplegeoprofiles.name_to_profile.get(triplegeo_profile_name)
        triplegeo_input_topio_id = \
            kg_conversion_information.input_file_topio_id
    except (KeyError, AttributeError):
        log_msg = 'Conversion tool TripleGeo was not configured properly'
        logger.error(log_msg)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=log_msg
        )

    if triplegeo_profile is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Conversion profile name '
                   f'"{triplegeo_profile_name}" not known'
        )

    triplegeo_input_file_path = get_file_path(triplegeo_input_topio_id)

    # TODO: Check whether file format matches triplegeo_profile.input_format
    # return status.HTTP_400_BAD_REQUEST if file format does not match

    try:
        triplegeo = TripleGeoRunner(
            triplegeo_executable_path=triplegeo_exec_path,
            profile=triplegeo_profile,
            input_files=[triplegeo_input_file_path],
            output_dir=working_dir)

    except WrongExecutablePath as e:
        # In case the TripleGeo executable path is mis-configured this will
        # cause an unrecoverable error
        logger.error(str(e))

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            # TODO: Rather not let the users know this internal message?
            detail='The RDF conversion process could not be run since the '
                   'TripleGeo executable path could not be found'
        )

    try:
        triplegeo.run()
    except RunnerExecutionFailed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='The RDF conversion process failed. Please check the input '
                   'file is in the correct format.')

    result_file_name = \
        get_file_name_base(triplegeo_input_file_path) + default_rdf_file_postfix
    triplegeo_result_file_path = os.path.join(working_dir, result_file_name)

    ############################################################################
    # Linking - LIMES
    #
    try:
        limes_cfg = cfg['limes']
        limes_exec_path = limes_cfg['executable_path']
        limes_target_topio_id = kg_conversion_information.topio_kg_topio_id
    except (KeyError, AttributeError):
        log_msg = 'Linking tool LIMES was not configured properly'
        logger.error(log_msg)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=log_msg
        )

    topio_kg_file_path = get_file_path(limes_target_topio_id)

    # TODO: Determine which linking profile to use based on metadata? So far we concentrate on POI data
    limes_profile = limesprofiles.slipo_equi_match_by_name_and_distance

    links_file_path = get_links_file_path(triplegeo_result_file_path)

    try:
        limes = LIMESRunner(
            limes_executable_path=limes_exec_path,
            profile=limes_profile,
            source_input_file_path=triplegeo_result_file_path,
            target_input_file_path=topio_kg_file_path,
            result_links_kg_file_path=links_file_path,
            output_dir=working_dir)

    except WrongExecutablePath as e:
        logger.error(str(e))

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            # TODO: Rather not let the users know this internal message?
            detail='The linking process could not be run since the LIMES '
                   'executable path could not be found'
        )

    try:
        limes.run()
    except RunnerExecutionFailed:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='The linking process failed due to an internal error.')

    ############################################################################
    # Data fusion - FAGI
    #
    try:
        # set up FAGI for data fusion
        fagi_cfg = cfg['fagi']
        fagi_exec_path = fagi_cfg['executable_path']

    except (KeyError, AttributeError):
        log_msg = 'Data fusion tool FAGI was not configured properly'
        logger.error(log_msg)

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=log_msg
        )

    # FIXME: Read through FAGI profiles again and choose appropriate mode
    fagi_profile = slipo_default_ab_mode
    fagi_profile.config.links.links_format = LinksFormat.NT

    try:
        fagi = FAGIRunner(
            fagi_executable_path=fagi_exec_path,
            profile=fagi_profile,
            left_input_file_path=triplegeo_result_file_path,
            right_input_file_path=topio_kg_file_path,
            links_file_path=links_file_path,
            output_dir_path=working_dir)

    except WrongExecutablePath as e:
        logger.error(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            # TODO: Rather not let the users know this internal message?
            detail='The data fusion process could not be run since the FAGI '
                   'executable path could not be found')

    try:
        fagi.run()

    except RunnerExecutionFailed:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='The data fusion process failed due to an internal error')

    # TODO: Write back result files to Topio Drive
    fused_dataset_file_path = os.path.join(
        working_dir, fagi_profile.config.target.fused)

    pid_service.register_asset(fused_dataset_file_path)
    fused_dataset_topio_id = pid_service.get_topio_id(fused_dataset_file_path)

    return KnowledgeGraphInfo(
        user_kg_topio_id=fused_dataset_topio_id,
        topio_kg_topio_id=kg_conversion_information.topio_kg_topio_id
    )


@gkgaas_app.post('/make_knowledge_graph', status_code=status.HTTP_201_CREATED)
def make_knowledge_graph(
        conversion_description: ConversionDescription,
        response: Response):

    working_dir = tempfile.mkdtemp()

    # set up TripleGeo...
    triplegeo_cfg = cfg['triplegeo']
    triplegeo_exec_path = triplegeo_cfg['executable_path']
    triplegeo_profile_name = \
        conversion_description.conversion_profile_name.lower()
    triplegeo_profile = \
        triplegeoprofiles.name_to_profile.get(triplegeo_profile_name)
    triplegeo_input_files = conversion_description.input_file_paths

    if triplegeo_profile is None:
        raise Exception(f'Conversion profile {triplegeo_profile_name} is not '
                        f'known.')

    # FIXME: has to fetch the files first!

    try:
        triplegeo = TripleGeoRunner(
            triplegeo_executable_path=triplegeo_exec_path,
            profile=triplegeo_profile,
            input_files=triplegeo_input_files,
            output_dir=working_dir)
    except WrongExecutablePath as e:
        # In case the TripleGeo executable path is mis-configured this will
        # cause an unrecoverable error
        logger.error(str(e))
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        # TODO: Rather not let the users know this internal message?
        response.body = 'The TripleGeo executable path could not be found'

        return response

    triplegeo.run()

    result_files = []
    result_file_paths = []
    for input_file in triplegeo_input_files:
        out_file_name = \
            get_file_name_base(input_file) + default_rdf_file_postfix

        out_file_path = os.path.join(working_dir, out_file_name)
        result_files.append(out_file_name)
        result_file_paths.append(out_file_path)

    if conversion_description.file_to_link_with is not None:
        print('Start linking')
        # ...then run LIMES
        limes_cfg = cfg['limes']
        limes_exec_path = limes_cfg['executable_path']
        limes_profile_name = conversion_description.linking_profile_name.lower()
        limes_target = conversion_description.file_to_link_with

        if limes_profile_name is None:
            # chosen randomly...
            limes_profile_name = limesprofiles.slipo_default_match

        limes_profile = limesprofiles.name_to_profile.get(limes_profile_name)

        if limes_profile is None:
            raise Exception(f'Linking profile {limes_profile_name} is not '
                            f'known')

        links_files = []
        for result_file_path in result_file_paths:
            links_file = get_links_file_path(result_file_path)

            limes = LIMESRunner(
                limes_executable_path=limes_exec_path,
                profile=limes_profile,
                source_input_file_path=result_file_path,
                target_input_file_path=limes_target,
                result_links_kg_file_path=links_file,
                output_dir=working_dir)

            limes.run()

            links_files.append(links_file)

        result_file_paths.append(limes_target)
        result_file_paths += links_files
        print('Linking done')

    # start SPARQL server with result files
    print('Starting fuseki...')
    fuseki_cfg = cfg['fuseki']
    fuseki_exec_path = fuseki_cfg['executable_path']
    sparql_server = FusekiWrapper(
        fuseki_exec_path,
        result_file_paths)

    sparql_server.run()

    # TODO: Move generated files to Topio file store
    # TODO: Delete working_dir!
    # TODO: Stop SPARQL server
