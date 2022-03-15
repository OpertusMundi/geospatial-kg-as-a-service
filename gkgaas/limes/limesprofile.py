import os
from dataclasses import dataclass
from enum import Enum
from typing import List


class DatasetType(Enum):
    SPARQL = 'SPARQL'
    CSV = 'CSV'
    N3 = 'N3'
    N_TRIPLES = 'N-TRIPLES'
    TURTLE = 'TURTLE'


class LIMESPlanner(Enum):
    DEFAULT = 'default'
    CANONICAL = 'canonical'
    HELIOS = 'helios'
    DYNAMIC = 'dynamic'


class LIMESRewriter(Enum):
    DEFAULT = 'default'
    ALGEBRAIC = 'algebraic'


class LIMESEngine(Enum):
    DEFAULT = 'default'
    SIMPLE = 'SIMPLE'
    PARTIAL_RECALL = 'PARTIAL_RECALL'


class LIMESMLAlgorithmName(Enum):
    WOMBAT_SIMPLE = 'WOMBAT Simple'
    WOMBAT_COMPLETE = 'WOMBAT Complete'
    EAGLE = 'EAGLE'
    DRAGON = 'DRAGON'


class LIMESMLAlgorithmType(Enum):
    SUPERVISED_BATCH = 'supervised batch'
    SUPERVISED_ACTIVE = 'supervised active'
    UNSUPERVISED = 'unsupervised'


class LIMESOutputFormat(Enum):
    TAB = 'TAB'
    CSV = 'CSV'
    NT = 'NT'
    TTL = 'TTL'


@dataclass
class Prefix:
    namespace: str
    label: str

    def __str__(self):
        return f"""    <PREFIX>
        <NAMESPACE>{self.namespace}</NAMESPACE>
        <LABEL>{self.label}</LABEL>
    </PREFIX>"""


@dataclass
class LIMESSource:
    id: str
    var: str
    properties: List[str]

    endpoint: str = None
    graph: str = None
    page_size: int = -1

    restrictions: List[str] = None
    min_offset: int = None
    max_offset: int = None
    dataset_type: DatasetType = DatasetType.SPARQL

    def __str__(self):
        if self.endpoint is None:
            raise Exception('endpoint URL was not initialized, yet')

        ret_str = f"""    <SOURCE>
        <ID>{self.id}</ID>
        <ENDPOINT>{self.endpoint}</ENDPOINT>""" + os.linesep

        if self.graph is not None:
            ret_str += f'        <GRAPH>{self.graph}</GRAPH>' + os.linesep

        ret_str += f"""        <VAR>{self.var}</VAR>
        <PAGESIZE>{self.page_size}</PAGESIZE>""" + os.linesep

        if self.min_offset is not None:
            ret_str += \
                f'        <MINOFFSET>{self.min_offset}</MINOFFSET>' + os.linesep

        if self.max_offset is not None:
            ret_str += \
                f'        <MAXOFFSET>{self.max_offset}</MAXOFFSET>' + os.linesep

        if self.restrictions:
            for restriction in self.restrictions:
                ret_str += \
                    f'        <RESTRICTION>{restriction}' \
                    f'</RESTRICTION>' + os.linesep
        else:
            ret_str += \
                f'        <RESTRICTION/>' + os.linesep

        for prop in self.properties:
            ret_str += f'        <PROPERTY>{prop}</PROPERTY>' + os.linesep

        ret_str += \
            f'        <TYPE>{self.dataset_type.value}</TYPE>' + os.linesep
        ret_str += '    </SOURCE>'

        return ret_str


@dataclass
class LIMESTarget:
    id: str
    var: str
    properties: List[str]

    endpoint: str = None
    graph: str = None
    page_size: int = -1
    restrictions: List[str] = None
    min_offset: int = None
    max_offset: int = None
    dataset_type: DatasetType = DatasetType.SPARQL

    def __str__(self):
        if self.endpoint is None:
            raise Exception('endpoint URL was not initialized, yet')

        ret_str = f"""    <TARGET>
        <ID>{self.id}</ID>
        <ENDPOINT>{self.endpoint}</ENDPOINT>""" + os.linesep

        if self.graph is not None:
            ret_str += f'        <GRAPH>{self.graph}</GRAPH>' + os.linesep

        ret_str += f"""        <VAR>{self.var}</VAR>
        <PAGESIZE>{self.page_size}</PAGESIZE>""" + os.linesep

        if self.min_offset is not None:
            ret_str += \
                f'        <MINOFFSET>{self.min_offset}</MINOFFSET>' + os.linesep

        if self.max_offset is not None:
            ret_str += \
                f'        <MAXOFFSET>{self.max_offset}</MAXOFFSET>' + os.linesep

        if self.restrictions:
            for restriction in self.restrictions:
                ret_str += \
                    f'        <RESTRICTION>{restriction}' \
                    f'</RESTRICTION>' + os.linesep
        else:
            ret_str += \
                f'        <RESTRICTION/>' + os.linesep

        for prop in self.properties:
            ret_str += f'        <PROPERTY>{prop}</PROPERTY>' + os.linesep

        ret_str += \
            f'        <TYPE>{self.dataset_type.value}</TYPE>' + os.linesep
        ret_str += '    </TARGET>'

        return ret_str


@dataclass
class LIMESExecution:
    rewriter: LIMESRewriter = LIMESRewriter.DEFAULT
    planner: LIMESPlanner = LIMESPlanner.DEFAULT
    engine: LIMESEngine = LIMESEngine.DEFAULT
    partial_recall_optimization_time: float = 0
    partial_recall_expected_selectivity: float = 1

    def __str__(self):
        ret_str = f"""    <EXECUTION>
        <REWRITER>{self.rewriter.value}</REWRITER>
        <PLANNER>{self.planner.value}</PLANNER>
        <ENGINE>{self.engine.value}</ENGINE>""" + os.linesep

        if self.engine == LIMESEngine.PARTIAL_RECALL:
            ret_str += \
                f'        <OPTIMIZATION_TIME>' \
                f'{self.partial_recall_optimization_time}' \
                f'</OPTIMIZATION_TIME>' + os.linesep

            ret_str += \
                f'        <EXPECTED_SELECTIVITY>' \
                f'{self.partial_recall_expected_selectivity}' \
                f'</EXPECTED_SELECTIVITY>' + os.linesep

        ret_str += '    </EXECUTION>'

        return ret_str


@dataclass
class LIMESMLAlgorithmParameter:
    name: str
    value: str

    def __str__(self):
        return f"""        <PARAMETER>
            <NAME>{self.name}</NAME>
            <VALUE>{self.value}</VALUE>
        </PARAMETER>"""


@dataclass
class LIMESMLAlgorithm:
    name: LIMESMLAlgorithmName
    algorithm_type: LIMESMLAlgorithmType
    training: str = None
    parameters: List[LIMESMLAlgorithmParameter] = None

    def __str__(self):
        ret_str = f"""    <MLALGORITHM>
        <NAME>{self.name.value}</NAME>
        <TYPE>{self.algorithm_type.value}</TYPE>""" + os.linesep

        if self.algorithm_type == LIMESMLAlgorithmType.SUPERVISED_BATCH:
            ret_str += \
                f'        <TRAINING>{self.training}</TRAINING>' + os.linesep

        if self.parameters is not None:
            for param in self.parameters:
                ret_str += \
                    f"""        <PARAMETER>
            <NAME>{param.name}</NAME>
            <VALUE>{param.value}</VALUE>
        </PARAMETER>""" + os.linesep

        ret_str += '    </MLALGORITHM>'

        return ret_str


@dataclass
class LIMESAcceptanceCondition:
    threshold: float
    file_path: str
    relation: str

    def __str__(self):
        return f"""    <ACCEPTANCE>
        <THRESHOLD>{self.threshold}</THRESHOLD>
        <FILE>{self.file_path}</FILE>
        <RELATION>{self.relation}</RELATION>
    </ACCEPTANCE>"""


@dataclass
class LIMESReviewCondition:
    threshold: float
    file_path: str
    relation: str

    def __str__(self):
        return f"""    <REVIEW>
        <THRESHOLD>{self.threshold}</THRESHOLD>
        <FILE>{self.file_path}</FILE>
        <RELATION>{self.relation}</RELATION>
    </REVIEW>"""


@dataclass
class LIMESProfile:
    _metadata = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE LIMES SYSTEM "limes.dtd">
<LIMES>"""
    _closing = '</LIMES>'

    source: LIMESSource
    target: LIMESTarget
    metric: str
    acceptance_condition: LIMESAcceptanceCondition
    review_condition: LIMESReviewCondition
    output_format: LIMESOutputFormat

    prefixes: List[Prefix] = None
    execution: LIMESExecution = LIMESExecution()
    ml_algorithm: LIMESMLAlgorithm = None
    granularity: int = None

    def to_config_file(self, config_file_path):
        with open(config_file_path, 'w') as config_file:
            config_file.write(self._metadata + os.linesep)

            if self.prefixes is not None:
                for prefix in self.prefixes:
                    config_file.write(str(prefix) + os.linesep)

            config_file.write(str(self.source) + os.linesep)
            config_file.write(str(self.target) + os.linesep)

            config_file.write(
                f'    <METRIC>{self.metric}</METRIC>' + os.linesep)

            if self.ml_algorithm is not None:
                config_file.write(str(self.ml_algorithm) + os.linesep)

            config_file.write(str(self.acceptance_condition) + os.linesep)
            config_file.write(str(self.review_condition) + os.linesep)

            config_file.write(str(self.execution) + os.linesep)

            if self.granularity is not None:
                config_file.write(
                    f'    <GRANULARITY>{self.granularity}</GRANULARITY>' +
                    os.linesep)

            config_file.write(
                f'    <OUTPUT>{self.output_format.value}</OUTPUT>' + os.linesep)

            config_file.write(self._closing)
