import os
import tempfile
from dataclasses import dataclass
from typing import List, Union, Optional, Tuple

from gkgaas.triplegeo import Runtime, InputFormat, ProcessingMode, \
    Serialization, Encoding
from gkgaas.triplegeo.classification import ClassificationSpecification
from gkgaas.triplegeo.mapping import MappingSpecification


class MissingSettingException(Exception):
    pass


@dataclass
class TripleGeoProfile(object):
    """
    Contains information/settings about how to do an automatic conversion of a
    specific input format possibly from a specific data source.
    """

    ###################################
    # required settings
    mapping_specification: MappingSpecification
    input_format: InputFormat
    key_attribute: str

    # Either one geometry column name, or the column names for x and y (long
    # and lat) coordinates
    geometry_attribute: Union[str, Tuple[str, str]]

    feature_source: str

    ###################################
    # settings usually added after object was initialized (and thus need an
    # initial value which, however, should be overridden later)
    input_files: List[str] = None
    output_dir: str = None

    ###################################
    # optional settings
    classification_specification: ClassificationSpecification = None
    name_attribute: Optional[str] = None
    category_attribute: Optional[str] = None
    ontology_namespace: Optional[str] = None
    geometry_namespace: Optional[str] = None
    feature_namespace: Optional[str] = None
    classification_scheme_namespace: Optional[str] = None
    class_namespace: Optional[str] = None
    data_source_namespace: Optional[str] = None
    namespaces: Optional[dict] = None
    source_crs: Optional[str] = None
    target_crs: Optional[str] = None
    default_language: str = 'en'
    runtime: Runtime = Runtime.JVM

    # TODO: Check whether this is needed
    # partitions: int = 3

    mode: ProcessingMode = ProcessingMode.STREAM
    tmp_dir: str = tempfile.gettempdir()
    batch_size: int = 10
    input_encoding: Encoding = Encoding.UTF_8
    output_serialization: Serialization = Serialization.N_TRIPLES
    target_geo_ontology: str = 'GeoSPARQL'

    # For consideration in the future:
    # classify_by_name: bool
    # delimiter: str = '|'
    # quote: str = '"'

    def to_config_file(self, config_file_path):
        nl = os.linesep

        with open(config_file_path, 'w') as config_file:
            # runtime
            config_file.write(f'runtime = {self.runtime.value}{nl}')

            # inputFormat
            supported_input_formats = [InputFormat.SHAPEFILE]

            if self.input_format not in supported_input_formats:
                raise Exception(
                    f'Input format {self.input_format} currently not supported')

            config_file.write(f'inputFormat = {self.input_format.value}{nl}')

            # mode
            config_file.write(f'mode = {self.mode.value}{nl}')

            # inputFiles
            input_files_value = ';'.join(self.input_files)
            config_file.write(f'inputFiles = {input_files_value}{nl}')

            # outputDir
            config_file.write(f'outputDir = {self.output_dir}{nl}')

            # tmpDir
            config_file.write(f'tmpDir = {self.tmp_dir}{nl}')

            # batchSize
            config_file.write(f'batchSize = {self.batch_size}{nl}')

            # encoding
            config_file.write(f'encoding = {self.input_encoding.value}{nl}')

            # delimiter  TODO: Implement

            # quote TODO: Implement

            # serialization
            config_file.write(
                f'serialization = {self.output_serialization.value}{nl}')

            # targetGeoOntology
            config_file.write(
                f'targetGeoOntology = {self.target_geo_ontology}{nl}')

            # mappingSpec
            file_path = \
                self.tmp_dir + os.sep + self.mapping_specification.file_name

            config_file.write(
                f'mappingSpec = {file_path}{nl}')

            # classificationSpec
            if self.class_namespace is not None:
                classification_spec_file = \
                    self.tmp_dir + \
                    os.sep + \
                    self.classification_specification.file_name

                config_file.write(
                    f'classificationSpec = {classification_spec_file}{nl}')

            # classifyByName TODO: Implement

            # attrKey
            config_file.write(f'attrKey = {self.key_attribute}{nl}')

            # attrGeometry / attrX + attrY
            if isinstance(self.geometry_attribute, Tuple):
                config_file.write(f'attrX = {self.geometry_attribute[0]}{nl}')
                config_file.write(f'attrY = {self.geometry_attribute[1]}{nl}')
            else:
                config_file.write(
                    f'attrGeometry = {self.geometry_attribute}{nl}')

            # attrName
            if self.name_attribute is not None:
                config_file.write(f'attrName = {self.name_attribute}{nl}')

            # attrCategory
            if self.category_attribute is not None:
                config_file.write(
                    f'attrCategory = {self.category_attribute}{nl}')

            # featureSource
            config_file.write(f'featureSource = {self.feature_source}{nl}')

            # nsOntology
            if self.ontology_namespace is not None:
                config_file.write(f'nsOntology = {self.ontology_namespace}{nl}')

            # nsGeometry
            if self.geometry_namespace is not None:
                config_file.write(f'nsGeometry = {self.geometry_namespace}{nl}')

            # nsFeatureURI
            if self.feature_namespace is not None:
                config_file.write(
                    f'nsFeatureURI = {self.feature_namespace}{nl}')

            # nsClassificationURI
            if self.classification_scheme_namespace is not None:
                config_file.write(
                    f'nsClassificationURI = '
                    f'{self.classification_scheme_namespace}{nl}')

            # nsClassURI
            if self.class_namespace is not None:
                config_file.write(f'nsClassURI = {self.class_namespace}{nl}')

            # nsDataSourceURI
            if self.data_source_namespace is not None:
                config_file.write(
                    f'nsDataSourceURI = {self.data_source_namespace}{nl}')

            # prefixes
            keys = [k for k in self.namespaces.keys()]

            if keys:
                values = [self.namespaces[k] for k in keys]

                keys_str = ', '.join(keys)
                vals_str = ', '.join(values)

                config_file.write(f'prefixes = {keys_str}{nl}')
                config_file.write(f'namespaces = {vals_str}{nl}')

            # sourceCRS
            if self.source_crs is not None:
                config_file.write(f'sourceCRS = {self.source_crs}{nl}')

            # targetCRS
            if self.target_crs is not None:
                config_file.write(f'targetCRS = {self.target_crs}{nl}')

            # defaultLang
            config_file.write(f'defaultLang = {self.default_language}')
