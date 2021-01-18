from enum import Enum


class Runtime(Enum):
    JVM = 'JVM'
    SPARK = 'SPARK'


class InputFormat(Enum):
    SHAPEFILE = 'SHAPEFILE'
    CSV = 'CSV'
    GPX = 'GPX'
    GEOJSON = 'GEOJSON'
    XML = 'XML'
    OSM_XML = 'OSM_XML'
    OSM_PBF = 'OSM_PBF'
    JSON = 'JSON'


class ProcessingMode(Enum):
    GRAPH = 'GRAPH'  # on disk
    STREAM = 'STREAM'  # in-memory
    RML = 'RML'  # for applying user-specified RML schema mappings
    XSLT = 'XSLT'  # for handling XML/GML/KML/INSPIRE-aligned input


class Serialization(Enum):
    RDF_XML = 'RDF/XML'
    RDF_XML_ABBREV = 'RDF/XML-ABBREV'
    N_TRIPLES = 'N-TRIPLES'
    TURTLE = 'TURTLE'
    N3 = 'N3'


class Encoding(Enum):
    ISO_8859_1 = 'ISO-8859-1'
    ISO_8859_7 = 'ISO-8859-7'
    WINDOWS_1253 = 'WINDOWS-1253'
    UTF_8 = 'UTF-8'  # default
