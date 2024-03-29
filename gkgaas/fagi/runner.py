import logging
import os
import shutil
import subprocess
import tempfile

from gkgaas.exceptions import WrongExecutablePath, RunnerExecutionFailed
from gkgaas.fagi.fagiprofile import FAGIProfile

logger = logging.getLogger(__name__)


class FAGIRunner(object):
    """
    Executes the FAGI data fusion tool.
    """

    def __init__(
            self,
            fagi_executable_path: str,
            profile: FAGIProfile,
            left_input_file_path: str,
            right_input_file_path: str,
            links_file_path: str,
            output_dir_path: str):

        if not os.path.exists(fagi_executable_path):
            raise WrongExecutablePath(
                f'FAGI executable path {fagi_executable_path} does not exist'
            )

        self.exec_path = fagi_executable_path
        self.profile: FAGIProfile = profile
        self.profile.config.left.file_path = left_input_file_path
        self.profile.config.right.file_path = right_input_file_path
        self.profile.config.links.file_path = links_file_path
        self.profile.config.target.output_dir = output_dir_path

    def run(self):
        tmp_dir = tempfile.mkdtemp()

        rules_file_path = os.path.join(tmp_dir, 'rules.xml')
        self.profile.rules.to_file(rules_file_path)

        self.profile.config.rules = rules_file_path
        config_file_path = os.path.join(tmp_dir, 'fagi_config.xml')
        wd = self.exec_path.rsplit(os.sep, 1)[0]

        self.profile.config.target.statistics = \
            os.path.join(wd, self.profile.config.target.statistics)

        self.profile.config.target.fused = \
            os.path.join(
                self.profile.config.target.output_dir,
                self.profile.config.target.fused)

        self.profile.config.to_file(config_file_path)

        try:
            output = subprocess.check_output(
                f'{self.exec_path} {config_file_path}',
                stderr=subprocess.STDOUT,
                shell=True,
                universal_newlines=True,
                cwd=wd)
        except subprocess.CalledProcessError as e:
            log_msg = \
                f'{self.exec_path} failed with return code {e.returncode}:' \
                f'\n{e.output}'
            logger.error(log_msg)

            shutil.rmtree(tmp_dir)
            raise RunnerExecutionFailed(log_msg)

        else:
            logger.debug(f'{self.exec_path} succeeded:\n{output}')
            shutil.rmtree(tmp_dir)
