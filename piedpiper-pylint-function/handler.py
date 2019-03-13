import os

from pylint import epylint
from .util import build_temp_zipfiles, build_directories, unzip_files


def handle(request):
    """
    handle a request to the function
    Args:
        request (str): request body
    """
    zip_files = build_temp_zipfiles(request)
    temp_directories = build_directories(request)
    pylint_reports = []
    for zip_file, temp_directory in zip(zip_files, temp_directories):
        unzip_files(zip_file, temp_directory.name)
        os.chdir(temp_directory.name)
        pylint_reports = run_pylint('.')

    return pylint_reports


def get_rcfile():
    """
    Looks in the file directory for the pylintrc file
    :return: None if file not found else returns fully qualified path
    """
    file_name = '.pylintrc'
    for (root, dir, files) in os.walk(os.path.dirname(__file__)):
        if file_name in files:
            return os.path.join(root, file_name)
    return None


def run_pylint(directory):
    """
    Runs pylint on the directory
    :param directory: string of directory (absolute or relative) to run pylint on
    :return: str of results
    """
    buffer = ''
    rcfile = get_rcfile()
    for (root, dir, files) in os.walk(directory):
        for file in files:
            full_path = os.path.abspath(os.path.join(root, file))
            if rcfile is not None:
                buffer += "Using pylintrc file : {}\n".format(rcfile)
                full_path += ' --rcfile={}'.format(rcfile)
            else:
                buffer += 'Could not locate pylintrc file\n'

            out, err = epylint.py_run(full_path, return_std=True)
            buffer += out.getvalue()
            buffer += err.getvalue()
    return buffer
