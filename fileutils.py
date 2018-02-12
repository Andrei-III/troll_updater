from os import remove
from os.path import isfile, isdir, exists, basename
from shutil import rmtree


def path_exists(path):
    if path is None:
        return False
    if not exists(path):
        return False
    return True


def dir_exists(dir_path):
    return path_exists(dir_path) and isdir(dir_path)


def file_exists(file_path):
    return path_exists(file_path) and isfile(file_path)


def get_filename(path):
    if not file_exists(path):
        return None
    return basename(path).split(".")[0]


def get_dirname(path):
    if not dir_exists(path):
        return None
    return basename(path)


# Removes a file and ignores errors
def remove_file_silent(file_path):
    try:
        remove(file_path)
    except OSError:
        pass


# Removes a directory and ignores errors
def remove_dir_silent(dir_path):
    if dir_exists(dir_path):
        rmtree(dir_path, ignore_errors=True)
