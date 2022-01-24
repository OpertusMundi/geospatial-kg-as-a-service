import os
import shutil
import subprocess
import tempfile

from rdflib import Graph, OWL, URIRef

from gkgaas.limes.limesprofile import LIMESProfile


class LIMESRunner(object):
    """
    Executes the LIMES linking tool to link a set of input datasets.
    """

    def __init__(
            self,
            limes_executable_path: str,
            profile: LIMESProfile,
            source_input_file_path: str,
            target_input_file_path: str,
            result_links_kg_file_path: str,
            output_dir: str):
        self.limes_executable_path = limes_executable_path
        self.profile = profile
        self.result_links_kg_file_path = result_links_kg_file_path
        self.output_dir = output_dir

        self.profile.source.endpoint = source_input_file_path
        self.profile.target.endpoint = target_input_file_path

    def _create_links_kg(self, accepted_links_file_path):
        """
        File content looks like this:

        <http://slipo.eu/id/poi/5f8cc6e3-bf91-3f7b-ad1a-23e480cd74d1>	<https://sws.geonames.org/9294554/>	0.9321554652991914
        <http://slipo.eu/id/poi/5f8cc6e3-bf91-3f7b-ad1a-23e480cd74d1>	<https://sws.geonames.org/9300183/>	0.9985261319810942
        <http://slipo.eu/id/poi/5f8cc6e3-bf91-3f7b-ad1a-23e480cd74d1>	<https://sws.geonames.org/261198/>	0.9042800408579729
        <http://slipo.eu/id/poi/5f8cc6e3-bf91-3f7b-ad1a-23e480cd74d1>	<https://sws.geonames.org/253825/>	0.9150961228550154
        """

        g = Graph()

        with open(accepted_links_file_path, 'r') as links_file:
            for line in links_file:
                if line.strip() == '':
                    continue
                left_iri_str, right_iri_str, confidence_score_str = line.split()

                g.add((URIRef(left_iri_str[1:-1]), OWL.sameAs, URIRef(right_iri_str[1:-1])))

        g.serialize(
            open(self.result_links_kg_file_path, 'wb'), format='ntriples')

    def run(self):
        tmp_dir = tempfile.mkdtemp()
        config_file_path = os.path.join(
            tmp_dir, 'limes_config_generated.properties')

        self.profile.to_config_file(config_file_path)

        wd = self.limes_executable_path.rsplit(os.sep, 1)[0]
        subprocess.run([self.limes_executable_path, config_file_path], cwd=wd)

        accepted_links_file_name = self.profile.acceptance_condition.file_path

        if not os.path.isabs(accepted_links_file_name):
            executable_dir = os.path.dirname(self.limes_executable_path)
            accepted_links_file_name = \
                os.path.join(executable_dir, accepted_links_file_name)

        self._create_links_kg(accepted_links_file_name)

        shutil.rmtree(tmp_dir)

