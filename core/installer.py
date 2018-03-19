import os_utils


def install_patch(dst_path, src_path):
    if os_utils.dir_exists(dst_path) and os_utils.dir_exists(src_path):
        os_utils.overwrite_dir(dst_path, src_path)
        return True
    else:
        return False


def install_addon(dst_path, src_path):
    return install_patch(dst_path, src_path)
