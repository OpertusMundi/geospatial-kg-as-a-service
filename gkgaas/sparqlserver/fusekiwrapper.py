import logging
import os
import subprocess
import time
from typing import List

from SPARQLWrapper import SPARQLWrapper, JSON

from gkgaas.exceptions import WrongExecutablePath
from gkgaas.sparqlserver import SPARQLServer

logger = logging.getLogger(__name__)


class FusekiWrapper(SPARQLServer):
    def __init__(
            self,
            path_to_fuseki_executable: str,
            rdf_file_paths: List[str],
            port: int = 8080):

        if not os.path.exists(path_to_fuseki_executable):
            raise WrongExecutablePath(
                f'Fuseki executable path {path_to_fuseki_executable} does '
                f'not exist'
            )

        for rdf_file_path in rdf_file_paths:
            if not os.path.exists(rdf_file_path):
                raise FileNotFoundError()

        self.path_to_fuseki_executable = path_to_fuseki_executable
        self.rdf_file_paths = rdf_file_paths
        self.port = port
        self.server_process = None

    def _get_query_url(self):
        hostname = os.uname().nodename

        return f'http://{hostname}:{self.port}/kg/sparql'

    def run(self):
        if self.server_process is not None:
            raise Exception('Service already running')

        args = [self.path_to_fuseki_executable]

        for file_path in self.rdf_file_paths:
            args.append(f'--file={file_path}')

        args.append(f'--port={self.port}')
        args.append('/kg')

        # /path/to/fuseki-server \
        #     --file=/tmp/file1.nt --file=/gkaas/file2.nt \
        #     /

        # Working directory is set s.t. Fuseki temp files won't mess up the
        # Git repo
        fuseki_dir = os.path.dirname(self.path_to_fuseki_executable)
        self.server_process = subprocess.Popen(args, cwd=fuseki_dir)

        logger.info(f'SPARQL server started at {self._get_query_url()}')

    def stop(self):
        logger.info('Stopping SPARQL server')
        if self.server_process is not None:
            self.server_process.kill()

    def query(self, sparql_query: str):
        url = self._get_query_url()
        sparql_endpoint = SPARQLWrapper(url)
        sparql_endpoint.setReturnFormat(JSON)
        sparql_endpoint.setQuery(sparql_query)

        return sparql_endpoint.queryAndConvert()
