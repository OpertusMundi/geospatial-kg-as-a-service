import os


def get_file_name_base(path: str) -> str:
    file_name = os.path.basename(path)

    return os.path.splitext(file_name)[0]


def get_links_file_path(file_path: str) -> str:
    """
    Given an RDF file path like /path/to/file.nt this will create a file path
    for the respective linking triples named /path/to/file_links.nt
    """

    path_w_base_name, suffix = os.path.splitext(file_path)

    return path_w_base_name + '_linked' + suffix
