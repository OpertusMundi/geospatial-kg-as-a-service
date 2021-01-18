from gkgaas.triplegeo import Runtime, InputFormat, ProcessingMode, Encoding, \
    Serialization
from gkgaas.triplegeo.preconfigs.classifications import \
    osm_poi_3_0_classification
from gkgaas.triplegeo.preconfigs.mappings import \
    osm_shapefile_mapping_specification
from gkgaas.triplegeo.profile import TripleGeoProfile

osm_shapefile_profile = TripleGeoProfile(
    runtime=Runtime.JVM,
    input_format=InputFormat.SHAPEFILE,
    mode=ProcessingMode.STREAM,
    batch_size=10,
    input_encoding=Encoding.UTF_8,
    output_serialization=Serialization.TURTLE,
    target_geo_ontology='GeoSPARQL',
    mapping_specification=osm_shapefile_mapping_specification,
    classification_specification=osm_poi_3_0_classification,
    key_attribute='osm_id',
    name_attribute='name',
    geometry_attribute=('lon', 'lat'),
    category_attribute='type',
    feature_source='OpenStreetMap',
    ontology_namespace='http://slipo.eu/def#',  # FIXME
    geometry_namespace='http://www.opengis.net/ont/geosparql#',
    feature_namespace='http://slipo.eu/id/poi/',
    classification_scheme_namespace='http://slipo.eu/id/classification/',
    class_namespace='http://slipo.eu/id/term/',
    data_source_namespace='http://slipo.eu/id/poisource/',
    namespaces={
        'slipo': 'http://slipo.eu/def#',
        'geo': 'http://www.opengis.net/ont/geosparql#',
        'xsd': 'http://www.w3.org/2001/XMLSchema#',
        'rdfs': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
        'wgs84_pos': 'http://www.w3.org/2003/01/geo/wgs84_pos#'
    },
    default_language='en')
