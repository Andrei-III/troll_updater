import os
import shutil
import sys
import httplib
import struct
import time
import urllib2
import zipfile
from colorama import init, Fore, Back, Style
from _winreg import *


def path_exists(path):
    if path is None:
        return False
    if not os.path.exists(path):
        return False
    return True


def dir_exists(dir_path):
    return path_exists(dir_path) and os.path.isdir(dir_path)


def file_exists(file_path):
    return path_exists(file_path) and os.path.isfile(file_path)


def get_filename(path):
    if not file_exists(path):
        return None
    return os.path.basename(path).split(".")[0]


def get_dirname(path):
    if not dir_exists(path):
        return None
    return os.path.basename(path)


# Removes a file and ignores errors
def remove_file_silent(file_path):
    try:
        os.remove(file_path)
    except OSError:
        pass


# Removes a directory and ignores errors
def remove_dir_silent(dir_path):
    if dir_exists(dir_path):
        shutil.rmtree(dir_path, ignore_errors=True)


def overwrite_dir(root_dst_dir, root_src_dir):
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


# Returns warband installation path if found and None otherwise
def get_warband_path():
    try:
        a_key = OpenKey(HKEY_LOCAL_MACHINE, r"SOFTWARE\mount&blade warband")
        install_path = QueryValueEx(a_key, "install_path")
        CloseKey(a_key)
        return install_path[0]
    except WindowsError:
        return None


# Returns True if the patch was found in the warband installation path and False otherwise
def patch_found(path):
    if dir_exists(path):
        if file_exists(path + r'\version'):
            return True
        else:
            return False
    else:
        return False


# Returns the latest available version from URL
# If URL is unreachable it terminates the execution of the program
def check_latest_version(url):
    header = {
        'User-Agent': 'Mozilla/5.0 (X11 Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 '
                      'Safari/537.11',
        'Accept': 'text/html',
        'Accept-Charset': 'ISO-8859-1,utf-8q=0.7,*q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,enq=0.8',
        'Connection': 'close'}

    request = urllib2.Request(url, headers=header)
    version = None
    try:
        version = urllib2.urlopen(request)
    except ValueError:
        error_color()
        print "\n  Invalid download URL: {0}".format(url)
        reset_colors()
        raw_input("\n  Press Enter to exit...")
        sys.exit(1)
    except urllib2.HTTPError as e:
        error_color()
        print "\n  Server failed to fulfill the request."
        print "Error code: {0}".format(e.code)
        reset_colors()
        raw_input("\n  Press Enter to exit...")
        sys.exit(1)
    except httplib.BadStatusLine:
        error_color()
        print "\n Invalid server response code " + version
        reset_colors()
        raw_input("\n  Press Enter to exit...")
        sys.exit(1)
    except urllib2.URLError as e:
        error_color()
        print "\n  Cannot reach server. Try again later."
        print "  Reason: {0}".format(e.reason)
        reset_colors()
        raw_input("\n  Press Enter to exit...")
        sys.exit(1)

    return version.read() if version is not None else None


# Creates a binary file that stores a packed integer which represents patch version
def create_version_file(path, version_int):
    if path is None or version_int is None:
        return False
    if not dir_exists(path):
        return False
    if not isinstance(version_int, int):
        return False
    if version_int < 0:
        return False
    version_file = open(path + r'\version', 'wb')
    version_file.write(struct.pack('i', version_int))
    version_file.close()
    return True


# Takes a string patch version (e.g. "1.2.1") and returns its integer version (e.g. 121)
# Returns None if version_str is invalid
def version_to_int(version_str):
    if version_str is None:
        return None
    if not isinstance(version_str, (basestring, str)):
        return None
    version = version_str.translate(None, ".")
    return int(version)


# Returns installed version in string format (e.g. "1.2.1")
def check_installed_version(path):
    if path is None:
        return None

    if not isinstance(path, (basestring, str, unicode)):
        return None

    version_path = path + r'\version'

    if not file_exists(version_path):
        return None

    with open(version_path, 'rb') as file_handle:
        version = struct.unpack('i', file_handle.read())[0]
        version_str = str(version)
        return version_str[0] + '.' + version_str[1] + '.' + version_str[2]


# Returns path to downloaded file
def download_file(download_url):
    print "\n  Requesting file download, please wait...",
    print "(this might take a while)\n"
    try:
        patch = urllib2.urlopen(download_url)
    except urllib2.HTTPError as e:
        print "  Failed to download file.\nReason: {0}".format(e)
        sys.exit(1)
    meta = patch.info()
    file_name = str(meta.getheaders("content-disposition")[0].split(';')[1].split("\"")[1])
    file_size = long(meta.getheaders("Content-Length")[0])
    filewriter = open(file_name, 'wb')
    print "  Downloading: %s  [ %s B ]" % (file_name, file_size)

    downloaded_bytes = 0
    block_sz = 8192
    progress = "%10d [%3.2f%%]" % (downloaded_bytes, downloaded_bytes * 100. / file_size)

    while True:
        download_buffer = patch.read(block_sz)

        if not download_buffer:
            break
        else:
            downloaded_bytes += len(download_buffer)
            filewriter.write(download_buffer)
            progress = r"%10d [%3.2f%%]" % (downloaded_bytes, downloaded_bytes * 100. / file_size)
            progress = progress + chr(8) * (len(progress) + 1)
            print progress,

    filewriter.close()
    print "  Download complete:",
    print progress
    return os.getcwd() + "\\" + file_name


# Returns path to extracted file
def extract_zip(zip_path):
    print "\n  Extracting archive ...",
    zip_ref = zipfile.ZipFile(zip_path, 'r')
    output_dir = zip_path.split(".")[0]
    zip_ref.extractall(output_dir)
    print "\tdone"
    zip_ref.close()
    return output_dir


# Archives a directory into a zip file
def backup_zip(dst_path, src_path):
    if dir_exists(dst_path) and dir_exists(src_path):
        print "\n  Creating backup ...",
        date = time.strftime("%Y-%m-%d_%H-%M-%S")
        backup_name = get_dirname(src_path) + "_Backup_" + date
        shutil.make_archive(dst_path + "\\" + backup_name, 'zip', src_path)
        print "\t\tdone"


# Removes a list of files and directories
# Returns True if successful and False otherwise
def clean_up(path_list):
    print "\n  Cleaning up ...",

    if path_list is None:
        error_color()
        print "\t\tfailed"
        reset_colors()
        return False

    for path in path_list:
        if dir_exists(path):
            remove_dir_silent(path)
            continue
        if file_exists(path):
            remove_file_silent(path)
    print "\t\tdone"
    return True


def install_patch(dst_path, src_path):
    print "\n  Installing {0}...".format(get_dirname(src_path)),
    if dir_exists(src_path):
        remove_dir_silent(dst_path)
        shutil.copytree(src_path, dst_path)
        print "\t\tdone"
    else:
        error_color()
        print "\tfailed"
        reset_colors()
        raw_input("\n  Press Enter to exit...")
        sys.exit(1)


def install_addon(dst_path, src_path):
    print "\n  Installing {0} ...".format(get_dirname(src_path)),
    if dir_exists(src_path):
        overwrite_dir(dst_path, src_path)
        print "\tdone"
    else:
        error_color()
        print "\tfailed"
        reset_colors()
        raw_input("\n  Press Enter to exit...")
        sys.exit(1)


def error_color():
    print Fore.LIGHTRED_EX


def success_color():
    print Fore.LIGHTGREEN_EX


def reset_colors():
    print Style.RESET_ALL


def print_logo():
    print "\n"
    print "\t  _____          _ _  ____                      "
    print "\t |_   _| __ ___ | | |/ ___| __ _ _ __ ___   ___ "
    print "\t   | || '__/ _ \| | | |  _ / _` | '_ ` _ \ / _ \\"
    print "\t   | || | | (_) | | | |_| | (_| | | | | | |  __/"
    print "\t   |_||_|  \___/|_|_|\____|\__,_|_| |_| |_|\___|"
    print "\t   _   _           _       _                    "
    print "\t  | | | |_ __   __| | __ _| |_ ___ _ __         "
    print "\t  | | | | '_ \ / _` |/ _` | __/ _ \ '__|        "
    print "\t  | |_| | |_) | (_| | (_| | ||  __/ |           "
    print "\t   \___/| .__/ \__,_|\__,_|\__\___|_|           "
    print "\t        |_|                                     "
    print "\t                                                "
    print "\t                              by LizardWizard   "
    print "\n\n"


def print_main_menu():
    installed_version = check_installed_version(NATIVE_PATH)
    print "  Warband found:     \t{0}\n".format(WARBAND_PATH)
    print "  Latest patch version:    \t{0}\n".format(LATEST_VERSION)
    print "  Installed patch version: \t{0}\n".format(
        installed_version if installed_version is not None else "not found")

    if installed_version is not None:
        print "  1. Update patch"
    else:
        print "  1. Install patch"
    print "  2. Install addons"
    print "  3. Exit"


def main_menu_handler(installed_patch_version):
    while True:
        choice = ask_input(['1', '2', '3'])
        if choice == '1':
            os.system("cls")
            print_logo()
            if installed_patch_version is None:  # Patch installation
                archive_path = download_file(PATCH_URL)
                archive_deflated_path = extract_zip(archive_path)
                backup_zip(MODULES_PATH, NATIVE_PATH)
                install_patch(NATIVE_PATH, archive_deflated_path + r"\TG-NeoGK\Native")
                create_version_file(NATIVE_PATH, version_to_int(LATEST_VERSION))
                clean_up([archive_deflated_path, archive_path])
                success_color()
                print "\n  TrollPatch installed successfully. Version: %s" % check_installed_version(NATIVE_PATH)
                reset_colors()
                raw_input("\n  Press Enter to return...")
                os.system('cls')
                print_logo()
                print_main_menu()
                main_menu_handler(check_installed_version(NATIVE_PATH))
                break
            elif installed_patch_version < LATEST_VERSION:  # Patch update
                archive_path = download_file(PATCH_URL)
                archive_deflated_path = extract_zip(archive_path)
                backup_zip(MODULES_PATH, NATIVE_PATH)
                install_patch(NATIVE_PATH, archive_deflated_path + r"\TG-NeoGK\Native")
                create_version_file(NATIVE_PATH, version_to_int(LATEST_VERSION))
                clean_up([archive_deflated_path, archive_path])
                success_color()
                print "\n  TrollPatch updated successfully. Version: %s" % check_installed_version(NATIVE_PATH)
                reset_colors()
                raw_input("\n  Press Enter to return...")
                os.system('cls')
                print_logo()
                print_main_menu()
                main_menu_handler(check_installed_version(NATIVE_PATH))
                break
            else:  # Patch is up-to-date already
                print "\n  Already up to date!\n"
                raw_input("\n  Press Enter to return...")
                os.system('cls')
                print_logo()
                print_main_menu()
                main_menu_handler(check_installed_version(NATIVE_PATH))
                break
        if choice == '2':
            os.system('cls')
            print_logo()
            print_addons_menu()
            addons_menu_handler()
            break
        if choice == '3':
            sys.exit(0)


def print_addons_menu():
    print " ", 21 * "-", "ADDONS", 21 * "-", "\n"
    print "  1. TrollGame Banner Pack"
    print "  2. Coughs addon"
    print "  3. Monty Python Theme addon"
    print "  4. Ni! addon"
    print "  5. Return to main menu"
    print "  6. Exit"
    print " ", 50 * "-"


def addons_menu_handler():
    while True:
        choice = ask_input(['1', '2', '3', '4', '5', '6'])
        if choice == '1':  # Install banner pack
            os.system("cls")
            print_logo()
            banners_zip = download_file(ADDON_BANNERS_URL)
            banners_unzip = extract_zip(banners_zip)
            install_addon(TEXTURES_PATH, banners_unzip + r'\Textures')
            clean_up([banners_zip, banners_unzip])
            success_color()
            print "\n  TrollGame Banner Pack installed successfully."
            reset_colors()
            raw_input("\n  Press Enter to return...")
            os.system('cls')
            print_logo()
            print_addons_menu()
            addons_menu_handler()
            break
        if choice == '2':  # Install coughs addon
            os.system("cls")
            print_logo()
            coughs_zip = download_file(ADDON_COUGHS_URL)
            coughs_unzip = extract_zip(coughs_zip)
            install_addon(SOUNDS_PATH, coughs_unzip + r'\Sounds')
            clean_up([coughs_zip, coughs_unzip])
            success_color()
            print "\n  Coughs addon installed successfully."
            reset_colors()
            raw_input("\n  Press Enter to return...")
            os.system('cls')
            print_logo()
            print_addons_menu()
            addons_menu_handler()
            break
        if choice == '3':  # Install monty python addon
            os.system("cls")
            print_logo()
            monty_zip = download_file(ADDON_MPTHEME_URL)
            monty_unzip = extract_zip(monty_zip)
            install_addon(SOUNDS_PATH, monty_unzip + r'\Sounds')
            clean_up([monty_zip, monty_unzip])
            success_color()
            print "\n  Monty Python Theme addon installed successfully."
            reset_colors()
            raw_input("\n  Press Enter to return...")
            os.system('cls')
            print_logo()
            print_addons_menu()
            addons_menu_handler()
            break
        if choice == '4':  # Install ni! addon
            os.system("cls")
            print_logo()
            ni_zip = download_file(ADDON_MPTHEME_URL)
            ni_unzip = extract_zip(ni_zip)
            install_addon(SOUNDS_PATH, ni_unzip + r'\Sounds')
            clean_up([ni_zip, ni_unzip])
            success_color()
            print "\n  Ni! addon installed successfully."
            reset_colors()
            raw_input("\n  Press Enter to return...")
            os.system('cls')
            print_logo()
            print_addons_menu()
            addons_menu_handler()
            break
        if choice == '5':  # Return to main menu
            os.system('cls')
            print_logo()
            print_main_menu()
            main_menu_handler(check_installed_version(NATIVE_PATH))
            break
        if choice == '6':  # Exit
            sys.exit(0)


def ask_input(valid_inputs):
    print ""
    while True:
        choice = raw_input("  > ")
        for arg in valid_inputs:
            if choice == arg:
                return choice


PATCH_URL = "https://www.dropbox.com/s/accz9cxgxpkswhv/TG-NeoGK.zip?dl=1"
ADDON_COUGHS_URL = "https://www.dropbox.com/s/3c3coi7xs9h7nid/Coughs.zip?dl=1"
ADDON_MPTHEME_URL = "https://www.dropbox.com/s/hwpa9ua7pe0t6kz/Monty.zip?dl=1"
ADDON_NI_URL = "https://www.dropbox.com/s/bw9tsomflz3a9hf/Ni.zip?dl=1"
ADDON_BANNERS_URL = "https://www.dropbox.com/s/19sbpbnrscu33ze/Banners.zip?dl=1"
VERSION_URL = "http://troll-game.org/api/neogk/version"
WARBAND_PATH = get_warband_path()
MODULES_PATH = WARBAND_PATH + r"\Modules"
NATIVE_PATH = MODULES_PATH + r"\Native"
SOUNDS_PATH = NATIVE_PATH + r"\Sounds"
TEXTURES_PATH = NATIVE_PATH + r"\Textures"

init()  # init colorama for colored console text
os.system("title TrollGame Updater v1.1.1")

# Warband installation not found
if WARBAND_PATH is None:
    print "  Warband not found."
    raw_input("\n  Press Enter to exit...")
    sys.exit(1)

print_logo()
print "\n  Connecting to server..."

LATEST_VERSION = check_latest_version(VERSION_URL)
os.system('cls')
print_logo()
print_main_menu()
main_menu_handler(check_installed_version(NATIVE_PATH))
