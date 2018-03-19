import sys
import urllib2

from core.installer import install_addon
from core.net import downloader
from core.version import *
from core.warband.wb_constants import *
from core.zip import zipper
from ui import logo
from ui_utils import *
from ui_constants import *


class AddonsMenu:
    """
    Class to facilitate displaying addons that are available for download
    and user choice handling.
    """

    def __init__(self, available_addons):
        """
        :param available_addons: A list of TrollAddon objects
        that the menu will be built around.
        """
        self.__available_addons = available_addons

    def show(self):
        """
        Prints a console menu that displays available addons to install.
        """
        if self.__available_addons:
            menu_header = 21 * "-" + "ADDONS" + 21 * "-" + "\n"
            menu_footer = 50 * "-"
            print_indented(menu_header, INDENTATION_AMOUNT - 1)
            for x in range(0, len(self.__available_addons)):
                addon = self.__available_addons[x]
                if wb_utils.is_addon_installed(addon_name=addon.get_name(), native_path=NATIVE_PATH):
                    installed_version = Version.read_version_file(NATIVE_PATH + "\\" +
                                                                  addon.get_name() +
                                                                  VERSION_FILE_EXT)
                else:
                    installed_version = "None"
                print_addon(x+1, addon.get_name(), addon.get_version(), installed_version)
            print_indented("{0}. Return".format(len(self.__available_addons) + 1))
            print_indented("{0}. Exit".format(len(self.__available_addons) + 2))
            print_indented(menu_footer, INDENTATION_AMOUNT - 1)
        else:
            print_indented("No addons available.")

    def handle(self, previous_menu):
        """
        Handles user choice input for an addon menu.

        :param previous_menu: The MainMenu object to return to when the return
        option is selected by the user
        of available addons to install
        """
        if self.__available_addons is not None and len(self.__available_addons) > 0:
            valid_choices = [str(self.get_return_option()),
                             str(self.get_exit_option())]
            for x in range(1, len(self.get_available_addons())+1):
                valid_choices.append(str(x))
            while True:
                choice = ask_input(valid_choices)
                if choice == str(self.get_return_option()):
                    clear_screen()
                    logo.draw()
                    previous_menu.show()
                    previous_menu.handle(self)
                    break
                elif choice == str(self.get_exit_option()):
                    sys.exit(0)
                else:
                    clear_screen()
                    logo.draw()
                    print_indented("Requesting file download, please wait...\n")
                    try:
                        addon_zip_path = downloader.get_file(self.__available_addons[int(choice)-1].get_url())
                    except urllib2.HTTPError as e:
                        print_indented(colors.format_error("Failed to download file.\nReason: {0}".format(e)))
                        raw_input(format_indented("Press Enter to return...", INDENTATION_AMOUNT+1, True))
                        clear_screen()
                        logo.draw()
                        self.show()
                        self.handle(previous_menu)
                        break
                    print format_indented(format_justified_left("Extracting files ..."), INDENTATION_AMOUNT+1, True),
                    addon_unzip_path = zipper.extract_zip(addon_zip_path)
                    print "done"
                    print format_indented(format_justified_left("Installing {0} ..."
                                                                .format(self.__available_addons[int(choice)-1]
                                                                        .get_name())),
                                          INDENTATION_AMOUNT+1,
                                          True),
                    if install_addon(NATIVE_PATH, addon_unzip_path):
                        print "done"
                    else:
                        print colors.format_error("failed")
                        raw_input(format_indented("Press Enter to exit...", INDENTATION_AMOUNT+1, True))
                        sys.exit(1)
                    print format_indented(format_justified_left("Cleaning up ..."), INDENTATION_AMOUNT + 1, True),
                    os_utils.remove_all_silent([addon_zip_path, addon_unzip_path])
                    print "done"
                    addon_version = Version.from_str(self.__available_addons[int(choice)-1].get_version())
                    addon_version.save_to_file(NATIVE_PATH, self.__available_addons[int(choice)-1].get_name())
                    print_indented(colors.format_success("{0} installed successfully."
                                                         .format(self.__available_addons[int(choice)-1].get_name())),
                                   INDENTATION_AMOUNT,
                                   True)
                    raw_input(format_indented("Press Enter to return...", INDENTATION_AMOUNT+1, True))
                    clear_screen()
                    logo.draw()
                    self.show()
                    self.handle(previous_menu)
                    break
        else:
            raw_input(format_indented("Press Enter to return...", INDENTATION_AMOUNT+1))
            clear_screen()
            logo.draw()
            previous_menu.show()
            previous_menu.handle(self)

    def get_available_addons(self):
        return self.__available_addons

    def get_return_option(self):
        return len(self.__available_addons) + 1

    def get_exit_option(self):
        return len(self.__available_addons) + 2
