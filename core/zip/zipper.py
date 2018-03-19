import shutil
import time
import zipfile

from core import os_utils
from core.exception.io import *


# Returns path to extracted file
def extract_zip(zip_path):
    if not os_utils.file_exists(zip_path):
        raise FileNotFoundException("File '{0}' does not exist.".format(zip_path))
    zip_ref = zipfile.ZipFile(zip_path, 'r')
    output_dir = zip_path.split(".")[0]
    zip_ref.extractall(output_dir)
    zip_ref.close()
    return output_dir


# Archives a directory into a zip file
def backup_zip(dst_path, src_path):
    if not os_utils.dir_exists(dst_path):
        raise DirectoryNotFoundException("Directory '{0}' does not exist.".format(dst_path))
    if not os_utils.dir_exists(src_path):
        raise DirectoryNotFoundException("Directory '{0}' does not exist.".format(src_path))
    date = time.strftime("%Y-%m-%d_%H-%M-%S")
    backup_name = os_utils.get_dirname(src_path) + "_Backup_" + date
    shutil.make_archive(dst_path + "\\" + backup_name, 'zip', src_path)
