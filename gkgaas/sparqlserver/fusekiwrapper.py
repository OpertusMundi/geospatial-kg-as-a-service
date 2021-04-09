import os
import subprocess
from typing import List

from gkgaas.sparqlserver import SPARQLServer


class FusekiWrapper(SPARQLServer):
    def __init__(
            self,
            path_to_fuseki_executable: str,
            rdf_file_paths: List[str],
            port: int = 8080):

        self.path_to_fuseki_executable = path_to_fuseki_executable
        self.rdf_file_paths = rdf_file_paths
        self.port = port
        self.server_process = None

    def run(self) -> str:
        if self.server_process is not None:
            raise Exception('Service already running')

        args = [self.path_to_fuseki_executable]

        for file_path in self.rdf_file_paths:
            args.append(f'--file={file_path}')

        args.append(f'--port={self.port}')
        args.append('/')

        # /path/to/fuseki-server \
        #     --file=/tmp/file1.nt --file=/gkaas/file2.nt \
        #     /

        # Working directory is set s.t. Fuseki temp files won't mess up the
        # Git repo
        fuseki_dir = os.path.dirname(self.path_to_fuseki_executable)
        self.server_process = subprocess.Popen(args, cwd=fuseki_dir)

        hostname = os.uname().nodename

        return f'http://{hostname}:{self.port}/'

    def stop(self):
        if self.server_process is not None:
            self.server_process.kill()
