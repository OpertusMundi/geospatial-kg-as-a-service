import os
import shutil
import tempfile
from unittest import TestCase

from gkgaas.triplegeo.preconfigs.mappings import \
    osm_shapefile_mapping_specification


class TestMappingSpecification(TestCase):
    def test_to_yml_dir(self):
        tmp_dir = tempfile.mkdtemp()
        osm_shapefile_mapping_specification.to_yml_dir(tmp_dir)
        generated_mappings_file_path = \
            tmp_dir + os.sep + osm_shapefile_mapping_specification.file_name

        osm_shapefile_mappings_file_path = \
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                'test_osm_shapefile_mappings.yml')

        with open(osm_shapefile_mappings_file_path, 'r') as mappings_file:
            expected = mappings_file.read().strip()

            with open(generated_mappings_file_path, 'r') as gen_mappings_file:
                actual = gen_mappings_file.read().strip()

            self.assertEqual(expected, actual)

        shutil.rmtree(tmp_dir)
