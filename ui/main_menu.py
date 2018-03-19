import sys
import urllib2

from core import os_utils
from core.exception.io import DirectoryNotFoundException
from core.installer import install_patch
from core.net import downloader
from core.patch import TrollPatch
from core.version import Version, VERSION_FILE_EXT
from core.warband.wb_constants import *
from core.zip import zipper
from ui import logo
from ui.ui_utils import *
from ui.ui_constants import JUSTIFY_AMOUNT


class PatchMenu:
    """
    Class to facilitate displaying the patch version
    that is available for download and
    user choice handling.
    """

    def __init__(self, patch):
        """
        :param patch: The TrollPatch object that contains the version
        and download URL of the latest trollpatch
        """
        self.__patch = patch

    def show(self):
        installed_version = Version.from_file(NATIVE_PATH + '\\' + TrollPatch.NAME + VERSION_FILE_EXT)
        latest_version = Version.from_str(self.__patch.get_version())
        print_indented("Warband found:     \t{0}\n".format(WARBAND_PATH))
        print_indented("Latest patch version:    \t{0}\n".format(latest_version.to_str()))
        installed_patch_version_str = "Installed patch version: \t{0}\n" \
            .format((colors.format_success(installed_version.to_str())
                     if installed_version.equals(latest_version)
                     else colors.format_error(installed_version.to_str()))
                    if installed_version is not None else colors.format_error("None"))

        if installed_version is None:
            print_indented(installed_patch_version_str)
            print_indented("1. Install patch")
        else:
            print_indented(installed_patch_version_str)
            print_indented("1. Update patch")
        print_indented("2. Install addons")
        print_indented("3. Exit")

    def handle(self, next_menu):
        while True:
            choice = ask_input(['1', '2', '3'])
            if choice == '1':
                clear_screen()
                logo.draw()
                installed_version = Version.from_file(NATIVE_PATH + '\\' + TrollPatch.NAME + VERSION_FILE_EXT)
                latest_version = Version.from_str(self.__patch.get_version())
                if installed_version is None or \
                        installed_version.compare_to(latest_version) < 0:  # Patch installation
                    print_indented("Requesting file download, please wait...\n")
                    try:
                        patch_zip_path = downloader.get_file(self.__patch.get_url())
                    except urllib2.HTTPError as e:
                        print_indented(colors.format_error("Failed to download {0}.\nReason: {1}"
                                                           .format(TrollPatch.NAME, e)))
                        raw_input(format_indented("Press Enter to exit...", INDENTATION_AMOUNT, True))
                        sys.exit(1)
                    print format_indented(format_justified_left("Extracting files ..."),
                                          INDENTATION_AMOUNT + 1,
                                          True),
                    patch_unzip_path = zipper.extract_zip(patch_zip_path)
                    print "done"
                    try:
                        print format_indented(format_justified_left("Creating backup ..."),
                                              INDENTATION_AMOUNT + 1,
                                              True),
                        zipper.backup_zip(MODULES_PATH, NATIVE_PATH)
                        print "done"
                    except DirectoryNotFoundException as e:
                        print colors.format_error("failed")
                        print_indented(e.message, new_line_before=True)
                        raw_input(format_indented("Press Enter to exit...", INDENTATION_AMOUNT+1, True))
                        sys.exit(1)
                    install_patch(NATIVE_PATH, patch_unzip_path + r"\TG-NeoGK\Native")
                    latest_version.save_to_file(NATIVE_PATH, TrollPatch.NAME)
                    print format_indented(format_justified_left("Cleaning up ..."),
                                          INDENTATION_AMOUNT + 1,
                                          True),
                    os_utils.remove_all_silent([patch_unzip_path, patch_zip_path])
                    print "done"
                    success_string = "TrollPatch {0} successfully. Version: {1}" \
                        .format("installed" if not installed_version else "updated",
                                Version.read_version_file(NATIVE_PATH + "\\" + TrollPatch.NAME + VERSION_FILE_EXT))
                    print_indented(colors.format_success(success_string), new_line_before=True)
                    raw_input(format_indented("Press Enter to return...", INDENTATION_AMOUNT+1, True))
                    clear_screen()
                    logo.draw()
                    self.show()
                    self.handle(next_menu)
                    break
                else:  # Patch is up-to-date already
                    print_indented("Already up to date!\n")
                    raw_input(format_indented("Press Enter to return...", INDENTATION_AMOUNT+1, True))
                    clear_screen()
                    logo.draw()
                    self.show()
                    self.handle(next_menu)
                    break
            if choice == '2':
                clear_screen()
                logo.draw()
                next_menu.show()
                next_menu.handle(self)
                break
            if choice == '3':
                sys.exit(0)
