import logging
import os
import shutil
import subprocess
import tempfile
from typing import List

from gkgaas.exceptions import WrongExecutablePath, RunnerExecutionFailed
from gkgaas.triplegeo.profile import TripleGeoProfile

logger = logging.getLogger(__name__)


class TripleGeoRunner(object):
    """
    Executes TripleGeo to convert geospatial data given a certain format to RDF

    It is assumed that there is an executable for TripleGeo which takes exactly
    one command line argument which is a file path pointing to the main config
    file (corresponding to a TripleGeoProfile).
    """

    def __init__(
            self,
            triplegeo_executable_path: str,
            profile: TripleGeoProfile,
            input_files: List[str],
            output_dir):

        if not os.path.exists(triplegeo_executable_path):
            raise WrongExecutablePath(
                f'TripleGeo executable path {triplegeo_executable_path} does '
                f'not exist'
            )

        self.exec_path = triplegeo_executable_path
        self.profile = profile
        self.input_files = input_files
        self.output_dir = output_dir

    def run(self):
        tmp_dir = tempfile.mkdtemp()
        self.profile.tmp_dir = tmp_dir

        self.profile.mapping_specification.to_yml_dir(tmp_dir)
        self.profile.input_files = self.input_files
        self.profile.output_dir = self.output_dir

        self.profile.classification_specification.to_yml_file(tmp_dir)

        conf_file_path = tmp_dir + os.sep + 'config_generated.properties'
        self.profile.to_config_file(conf_file_path)
        wd = self.exec_path.rsplit(os.sep, 1)[0]

        try:
            output = subprocess.check_output(
                f'{self.exec_path} {conf_file_path}',
                stderr=subprocess.STDOUT,
                shell=True,
                universal_newlines=True,
                cwd=wd)

        except subprocess.CalledProcessError as e:
            log_msg = \
                f'{self.exec_path} failed with return code {e.returncode}:' + \
                f'\n{e.output}'
            logger.error(log_msg)

            shutil.rmtree(tmp_dir)
            raise RunnerExecutionFailed(log_msg)

        else:
            logger.debug(f'{self.exec_path} succeeded:\n{output}')
            shutil.rmtree(tmp_dir)
