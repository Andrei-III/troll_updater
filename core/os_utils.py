import os
import shutil

from ui import colors
from ui.ui_constants import *


def path_exists(path):
    """
    Checks if a path exists.

    :param path: The absolute path.
    :return: True if the path exists or False otherwise
    """
    if path is None:
        return False
    if not os.path.exists(path):
        return False
    return True


def dir_exists(dir_path):
    """
    Checks if a directory exists.

    :param dir_path: The absolute path of the directory.
    :return: True if the path exists and is a directory or False otherwise.
    """
    return path_exists(dir_path) and os.path.isdir(dir_path)


def file_exists(file_path):
    """
    Checks if a file exists.

    :param file_path: The absolute path of the file.
    :return: True if the path exists and is a file or False otherwise.
    """
    return path_exists(file_path) and os.path.isfile(file_path)


def find_first_file(root_dir, file_name):
    """
    Searches for a file in a given path recursively.

    :param root_dir: The root directory in which the file will be searched for.
    :param file_name: The file name to search for (including extension)
    :return: Path to the first file occurrence if the file was found or None otherwise.
    """
    if root_dir is None:
        return None

    for root, dirs, files in os.walk(root_dir):
        for current_file in files:
            if os.path.basename(current_file) == file_name:
                return os.path.join(root, current_file)
    return None


def get_filename(path):
    """
    Extracts the file name from an absolute path.

    :param path: The absolute path of the file.
    :return: File name or None if the file does not exist.
    """
    if not file_exists(path):
        return None
    return os.path.basename(path).split(".")[0]


def get_dirname(path):
    """
    Extracts the directory name from an absolute path.

    :param path: The absolute path of the directory.
    :return: Directory name or None if the directory does not exist.
    """
    if not dir_exists(path):
        return None
    return os.path.basename(path)


def remove_file_silent(file_path):
    """
    Removes a file ignoring errors.

    :param file_path: The path of the file that will be removed.
    """
    try:
        os.remove(file_path)
    except OSError:
        pass


def remove_dir_silent(dir_path):
    """
    Removes a directory ignoring errors.

    :param dir_path: The path of the directory that will be removed.
    """
    if dir_exists(dir_path):
        shutil.rmtree(dir_path, ignore_errors=True)


def remove_all_silent(path_list):
    """
    Removes a list of files and directories.

    :param path_list: The list of paths of the files and dirs that will be removed
    :return: True if the operation was successful or False otherwise
    """
    if path_list is None:
        print colors.format_error("failed")
        return False

    for path in path_list:
        if dir_exists(path):
            remove_dir_silent(path)
            continue
        if file_exists(path):
            remove_file_silent(path)
    return True


def overwrite_dir(root_dst_dir, root_src_dir):
    """
    Copies all files and directories from the source directory
    into the destination directory, overwriting them.

    :param root_dst_dir: The destination directory.
    :param root_src_dir: The source directory.
    """
    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.move(src_file, dst_dir)
