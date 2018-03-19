import httplib
import os
import sys
import urllib2

from core.net import downloader
from core.parse import json_parser
from core.warband.wb_constants import *
from ui import logo
from ui.addons_menu import AddonsMenu
from ui.main_menu import PatchMenu
from ui.ui_utils import *

# GLOBALS
API = 'https://troll-game.org/api/neogk'
APP_VERSION = "1.2.1"

# INIT
os.system("title TrollGame Updater v" + APP_VERSION)
logo.draw()

# Getting Warband installation path
if WARBAND_PATH is None:
    print_indented("Warband not found.")
    raw_input(format_indented("Press Enter to exit...", INDENTATION_AMOUNT+1, True))
    sys.exit(1)

# Getting metadata about available downloads from the server
clear_screen()
logo.draw()
print_indented("Connecting to server...", new_line_before=True)
try:
    JSON_RAW = downloader.get_json(API)
except ValueError:
    print_indented(colors.format_error("Invalid URL: {0}".format(API)), new_line_before=True)
    raw_input(format_indented("Press Enter to exit...", INDENTATION_AMOUNT + 1, True))
    sys.exit(1)
except urllib2.HTTPError as e:
    print_indented(colors.format_error("Server failed to fulfill the request."), new_line_before=True)
    print_indented(colors.format_error("Error code: {0}".format(e.code)))
    raw_input(format_indented("Press Enter to exit...", INDENTATION_AMOUNT + 1, True))
    sys.exit(1)
except httplib.BadStatusLine as e:
    print_indented(colors.format_error("Invalid server response code " + e.line), new_line_before=True)
    raw_input(format_indented("Press Enter to exit...", INDENTATION_AMOUNT + 1, True))
    sys.exit(1)
except urllib2.URLError as e:
    print_indented(colors.format_error("Cannot reach server. Try again later."), new_line_before=True)
    print_indented(colors.format_error("Reason: {0}".format(e.reason)))
    raw_input(format_indented("Press Enter to exit...", INDENTATION_AMOUNT + 1, True))
    sys.exit(1)
TROLL_PATCH = json_parser.get_troll_patch(JSON_RAW)
AVAILABLE_ADDONS = json_parser.get_troll_addons(JSON_RAW)
MAIN_MENU = PatchMenu(TROLL_PATCH)
ADDONS_MENU = AddonsMenu(AVAILABLE_ADDONS)
clear_screen()
logo.draw()
MAIN_MENU.show()
MAIN_MENU.handle(ADDONS_MENU)
