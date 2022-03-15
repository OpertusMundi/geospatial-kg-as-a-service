import unittest
from datetime import date

from starlette.datastructures import URL

from gkgaas.fagi import LinksFormat, FusionMode
from gkgaas.fagi.filesettings import LinksFileSettings, \
    LeftInputDatasetSettings, RightInputDatasetSettings, \
    FusedOutputDatasetSettings


class LeftInputDatasetSettingsTests(unittest.TestCase):
    def test_to_str_01(self):
        expected_config_str = """    <left>
        <id>a</id>
        <date>2022-06-01</date>
        <file>/path/to/dataset.nt</file>
    </left>"""

        input_dataset_settings = LeftInputDatasetSettings(
            id='a',
            date=date(year=2022, month=6, day=1),
            file_path='/path/to/dataset.nt'
        )

        self.assertEqual(expected_config_str, str(input_dataset_settings))

    def test_to_str_02(self):
        expected_config_str = """    <left>
        <id>b</id>
        <date>2022-05-13</date>
        <endpoint>http://dbpedia.org/sparql</endpoint>
    </left>"""

        input_dataset_settings = LeftInputDatasetSettings(
            id='b',
            date=date(year=2022, month=5, day=13),
            endpoint=URL('http://dbpedia.org/sparql')
        )

        self.assertEqual(expected_config_str, str(input_dataset_settings))

    def test_to_str_03(self):
        expected_config_str = """    <left>
        <id>a</id>
        <file>/path/to/dataset.nt</file>
    </left>"""

        input_dataset_settings = LeftInputDatasetSettings(
            id='a',
            file_path='/path/to/dataset.nt'
        )

        self.assertEqual(expected_config_str, str(input_dataset_settings))

    def test_to_str_04(self):
        input_dataset_settings = LeftInputDatasetSettings(
            id='a'
        )

        self.assertRaises(Exception, input_dataset_settings.__str__)


class RightInputDatasetSettingsTests(unittest.TestCase):
    def test_to_str_01(self):
        expected_config_str = """    <right>
        <id>a</id>
        <date>2022-06-01</date>
        <file>/path/to/dataset.nt</file>
    </right>"""

        input_dataset_settings = RightInputDatasetSettings(
            id='a',
            date=date(year=2022, month=6, day=1),
            file_path='/path/to/dataset.nt'
        )

        self.assertEqual(expected_config_str, str(input_dataset_settings))

    def test_to_str_02(self):
        expected_config_str = """    <right>
        <id>b</id>
        <date>2022-05-13</date>
        <endpoint>http://dbpedia.org/sparql</endpoint>
    </right>"""

        input_dataset_settings = RightInputDatasetSettings(
            id='b',
            date=date(year=2022, month=5, day=13),
            endpoint=URL('http://dbpedia.org/sparql')
        )

        self.assertEqual(expected_config_str, str(input_dataset_settings))

    def test_to_str_03(self):
        expected_config_str = """    <right>
        <id>a</id>
        <file>/path/to/dataset.nt</file>
    </right>"""

        input_dataset_settings = RightInputDatasetSettings(
            id='a',
            file_path='/path/to/dataset.nt'
        )

        self.assertEqual(expected_config_str, str(input_dataset_settings))

    def test_to_str_04(self):
        input_dataset_settings = RightInputDatasetSettings(
            id='a'
        )

        self.assertRaises(Exception, input_dataset_settings.__str__)


class TestLinksFileSettings(unittest.TestCase):
    def test_to_str_01(self):
        expected_config_str = """    <links>
        <id>links</id>
        <linksFormat>nt</linksFormat>
        <file>/path/to/file.nt</file>
    </links>"""

        links_file_settings = LinksFileSettings(
            id='links',
            file_path='/path/to/file.nt',
            links_format=LinksFormat.NT
        )

        self.assertEqual(expected_config_str, str(links_file_settings))

    def test_to_str_02(self):
        expected_config_str = """    <links>
        <id>links</id>
        <linksFormat>csv</linksFormat>
        <file>/path/to/file.csv</file>
    </links>"""

        links_file_settings = LinksFileSettings(
            id='links',
            file_path='/path/to/file.csv',
            links_format=LinksFormat.CSV
        )

        self.assertEqual(expected_config_str, str(links_file_settings))

    def test_to_str_03(self):
        expected_config_str = """    <links>
        <id>links</id>
        <linksFormat>csv-unique-links</linksFormat>
        <file>/path/to/file.csv</file>
    </links>"""

        links_file_settings = LinksFileSettings(
            id='links',
            file_path='/path/to/file.csv',
            links_format=LinksFormat.CSV_UNIQUE_LINKS
        )

        self.assertEqual(expected_config_str, str(links_file_settings))

    def test_to_str_04(self):
        expected_config_str = """    <links>
        <id>links</id>
        <linksFormat>csv-ensembles</linksFormat>
        <file>/path/to/file.csv</file>
    </links>"""

        links_file_settings = LinksFileSettings(
            id='links',
            file_path='/path/to/file.csv',
            links_format=LinksFormat.CSV_ENSEMBLES
        )

        self.assertEqual(expected_config_str, str(links_file_settings))


class TestFusedOutputDatasetSettings(unittest.TestCase):
    def test_to_str_01(self):
        expected_settings_str = """    <target>
        <id>fused</id>
        <mode>aa_mode</mode>
        <outputDir>/path/to/dir/</outputDir>
        <fused>fused.nt</fused>
        <remaining>remaining.nt</remaining>
        <ambiguous>ambiguous.nt</ambiguous>
        <statistics>statistics.txt</statistics>
        <fusionLog>fusionLog.txt</fusionLog>
    </target>"""

        output_dataset_settings = FusedOutputDatasetSettings(
            id='fused',
            mode=FusionMode.AA,
            output_dir='/path/to/dir/'
        )

        self.assertEqual(expected_settings_str, str(output_dataset_settings))

    def test_to_str_02(self):
        expected_settings_str = """    <target>
        <id>fused</id>
        <mode>bb_mode</mode>
        <outputDir>/path/to/dir/</outputDir>
        <fused>fused_file.nt</fused>
        <remaining>remaining_file.nt</remaining>
        <ambiguous>ambiguous_file.nt</ambiguous>
        <statistics>statistics_file.txt</statistics>
        <fusionLog>fusion_log.txt</fusionLog>
    </target>"""

        output_dataset_settings = FusedOutputDatasetSettings(
            id='fused',
            mode=FusionMode.BB,
            output_dir='/path/to/dir/',
            fused='fused_file.nt',
            remaining='remaining_file.nt',
            ambiguous='ambiguous_file.nt',
            statistics='statistics_file.txt',
            fusion_log='fusion_log.txt'
        )

        self.assertEqual(expected_settings_str, str(output_dataset_settings))

    def test_to_str_03(self):
        expected_settings_str = """    <target>
        <id>fused</id>
        <mode>l_mode</mode>
        <outputDir>/path/to/dir/</outputDir>
        <fused>fused.nt</fused>
        <remaining>remaining.nt</remaining>
        <ambiguous>ambiguous.nt</ambiguous>
        <statistics>statistics.txt</statistics>
        <fusionLog>fusionLog.txt</fusionLog>
    </target>"""

        output_dataset_settings = FusedOutputDatasetSettings(
            id='fused',
            mode=FusionMode.L,
            output_dir='/path/to/dir/'
        )

        self.assertEqual(expected_settings_str, str(output_dataset_settings))
