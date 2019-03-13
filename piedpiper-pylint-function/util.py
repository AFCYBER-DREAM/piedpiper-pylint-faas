import tempfile
import zipfile


def build_temp_zipfiles(request):
    zip_files = []
    for zip_file in request.files.getlist("files"):
        tmp_file = tempfile.NamedTemporaryFile(delete=False)
        tmp_file.write(zip_file.read())
        tmp_file.flush()
        zip_files.append(tmp_file.name)
    return zip_files

def build_directories(request):

    temp_directories = []
    for _ in request.files.getlist("files"):
        temp_directory = tempfile.TemporaryDirectory()
        temp_directories.append(temp_directory)

    return temp_directories

def unzip_files(zip_file, temp_directory):
    zip_ref = zipfile.ZipFile(zip_file, 'r')
    zip_ref.extractall(temp_directory)
    zip_ref.close()
