import filecmp
import os
import shutil
import tempfile
import unittest

from gkgaas.fagi import SerializationFormat, Locale, Similarity, \
    StatsLevelOfDetail, LinksFormat, FusionMode
from gkgaas.fagi.config import FAGIConfig
from gkgaas.fagi.filesettings import LeftInputDatasetSettings, \
    RightInputDatasetSettings, LinksFileSettings, FusedOutputDatasetSettings


class TestConfig(unittest.TestCase):
    def test_to_file_01(self):
        import tests.fagi
        project_dir = os.path.dirname(tests.fagi.__file__)
        expected_file_path = os.path.join(project_dir, 'config_01.xml')

        config = FAGIConfig(
            input_format=SerializationFormat.NT,
            output_format=SerializationFormat.NT,
            locale=Locale.EN,
            similarity=Similarity.JARO_WINKLER,
            verbose=True,
            stats=StatsLevelOfDetail.LIGHT,
            rules='rules.xml',
            left=LeftInputDatasetSettings(
                id='a',
                file_path='/path/to/left_input_file.nt'
            ),
            right=RightInputDatasetSettings(
                id='b',
                file_path='/path/to/right_input_file.nt'
            ),
            links=LinksFileSettings(
                id='links',
                links_format=LinksFormat.CSV_UNIQUE_LINKS,
                file_path='/path/to/links.csv'
            ),
            target=FusedOutputDatasetSettings(
                id='fused',
                mode=FusionMode.AB,
                output_dir='/path/to/output_dir/',
                fused='fused.nt',
                remaining='remaining.nt',
                ambiguous='ambiguous.nt',
                statistics='stats.txt',
                fusion_log='log.txt'
            )
        )

        tmp_dir = tempfile.mkdtemp()
        result_file_path = os.path.join(tmp_dir, 'config.xml')
        config.to_file(result_file_path)

        self.assertTrue(
            filecmp.cmp(expected_file_path, result_file_path),
            'Generated rules file content does not match the expected content')

        shutil.rmtree(tmp_dir)
