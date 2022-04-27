import logging
import logging.config
import os
import tempfile

import yaml
from fastapi import FastAPI
from fastapi import Response
from fastapi import status

import gkgaas.limes.preconfigs.profiles as limesprofiles
import gkgaas.triplegeo.preconfigs.profiles as triplegeoprofiles
from gkgaas.exceptions import WrongExecutablePath
from gkgaas.limes.runner import LIMESRunner
from gkgaas.model import ConversionDescription
from gkgaas.sparqlserver.fusekiwrapper import FusekiWrapper
from gkgaas.triplegeo.runner import TripleGeoRunner
from gkgaas.utils.paths import get_file_name_base, get_links_file_path

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
