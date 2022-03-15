from dataclasses import dataclass

from gkgaas.fagi import SerializationFormat, Locale, Similarity, \
    StatsLevelOfDetail
from gkgaas.fagi.filesettings import LeftInputDatasetSettings, \
    RightInputDatasetSettings, LinksFileSettings, FusedOutputDatasetSettings


@dataclass
class FAGIConfig:
    input_format: SerializationFormat
    output_format: SerializationFormat

    left: LeftInputDatasetSettings
    right: RightInputDatasetSettings
    links: LinksFileSettings
    target: FusedOutputDatasetSettings

    stats: StatsLevelOfDetail = StatsLevelOfDetail.LIGHT
    verbose: bool = False

    # Absolute path to the "rules.xml" file
    rules: str = None

    # TODO: ML settings

    locale: Locale = None
    similarity: Similarity = Similarity.JARO_WINKLER

    def to_file(self, file_path: str):
        config_str = f"""<?xml version="1.0" encoding="UTF-8"?>
<specification>
    <inputFormat>{str(self.input_format)}</inputFormat>
    <outputFormat>{str(self.output_format)}</outputFormat>
"""

        if self.locale is not None:
            config_str += f'    <locale>{str(self.locale)}</locale>\n'

        config_str += f"""    <similarity>{str(self.similarity)}</similarity>
    <verbose>{str(self.verbose).lower()}</verbose>
    <stats>{str(self.stats)}</stats>
    <rules>{self.rules}</rules>
{str(self.left)}
{str(self.right)}
{str(self.links)}
{str(self.target)}
    <ML>
    </ML>
</specification>
"""

        with open(file_path, 'w') as out_file:
            out_file.write(config_str)
