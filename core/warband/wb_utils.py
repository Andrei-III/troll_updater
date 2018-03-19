from _winreg import *

from core.os_utils import find_first_file
from core.patch import TrollPatch
from core.version import VERSION_FILE_EXT


def get_warband_path():
    """
    Attempts to locate the warband installation directory
    from the windows registry.

    :return: The warband installation path if found
    or None otherwise.
    """
    try:
        a_key = OpenKey(HKEY_LOCAL_MACHINE, r"SOFTWARE\mount&blade warband")
        install_path = QueryValueEx(a_key, "install_path")
        CloseKey(a_key)
        return install_path[0]
    except WindowsError:
        return None


def is_addon_installed(addon_name, native_path):
    """
    Checks if the addon is installed in the native directory.

    :param addon_name: The file name of the addon (excluding extension)
    :param native_path: The absolute path of the native directory of warband.
    :return: True if the addon version file was found or False otherwise.
    """
    if addon_name is None or native_path is None:
        return False

    return True if find_first_file(native_path,
                                   addon_name + VERSION_FILE_EXT) else False


def is_patch_installed(native_path):
    """
    Checks if the patch is installed in the native directory.

    :param native_path: The absolute path of the native directory of warband.
    :return: True if the patch version file was found or False otherwise.
    """
    return True if find_first_file(native_path, TrollPatch.NAME + VERSION_FILE_EXT) else False
