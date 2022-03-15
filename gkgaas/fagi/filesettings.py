from datetime import date
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from starlette.datastructures import URL

from gkgaas.fagi import LinksFormat, FusionMode


@dataclass
class FileSettings(ABC):
    id: str
    _prefix: str = field(init=False)

    @abstractmethod
    def __str__(self):
        pass


@dataclass
class InputDatasetSettings(FileSettings):
    # categories: List[str] = None  FIXME: not clear how to use this
    date: date = None
    file_path: str = None
    endpoint: URL = None

    def __str__(self):
        # self.id
        settings_str = f'        <id>{self.id}</id>'

        # self.date
        if self.date is not None:
            date_str = self.date.strftime('%Y-%m-%d')
            settings_str += f'\n        <date>{date_str}</date>'

        # self.file_path
        if self.file_path is not None:
            settings_str += f'\n        <file>{self.file_path}</file>'

        # self.endpoint
        else:
            if self.endpoint is None:
                raise Exception(
                    'Either file path or SPARQL endpoint has to be configured')

            settings_str += f'\n        <endpoint>{str(self.endpoint)}</endpoint>'

        return f'    <{self._prefix}>\n' + \
               settings_str + \
               f'\n    </{self._prefix}>'


class LeftInputDatasetSettings(InputDatasetSettings):
    _prefix = 'left'


class RightInputDatasetSettings(InputDatasetSettings):
    _prefix = 'right'


@dataclass
class LinksFileSettings(FileSettings):
    links_format: LinksFormat
    file_path: str = None

    _prefix = 'links'

    def __str__(self):
        return f"""    <{self._prefix}>
        <id>{self.id}</id>
        <linksFormat>{str(self.links_format)}</linksFormat>
        <file>{self.file_path}</file>
    </{self._prefix}>"""


@dataclass
class FusedOutputDatasetSettings(FileSettings):
    mode: FusionMode
    output_dir: str = None

    # Optional. Specifies the output file path of the fused dataset (based on
    # the fusion mode).
    fused: str = 'fused.nt'

    # Optional. Specifies the output file path of the non-fused dataset (based
    # on the fusion mode).
    remaining: str = 'remaining.nt'

    # Optional. Specifies the output file path of the dataset containing
    # ambiguous linked entities.
    ambiguous: str = 'ambiguous.nt'

    statistics: str = 'statistics.txt'
    fusion_log: str = 'fusionLog.txt'

    _prefix = 'target'

    def __str__(self):
        return f"""    <{self._prefix}>
        <id>{self.id}</id>
        <mode>{str(self.mode)}</mode>
        <outputDir>{self.output_dir}</outputDir>
        <fused>{self.fused}</fused>
        <remaining>{self.remaining}</remaining>
        <ambiguous>{self.ambiguous}</ambiguous>
        <statistics>{self.statistics}</statistics>
        <fusionLog>{self.fusion_log}</fusionLog>
    </{self._prefix}>"""
