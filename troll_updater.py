import sys
import httplib
import shutil
import struct
import time
import urllib2
import zipfile
from _winreg import *
from os import getcwd, system

import fileutils


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
    if fileutils.dir_exists(path):
        if fileutils.file_exists(path + r'\version'):
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
        print "\n  Invalid download URL: {0}".format(url)
        raw_input("\n  Press Enter to exit...")
        sys.exit(1)
    except urllib2.HTTPError as e:
        print "\n  Server failed to fulfill the request."
        print "Error code: {0}".format(e.code)
        raw_input("\n  Press Enter to exit...")
        sys.exit(1)
    except httplib.BadStatusLine:
        print "\n Invalid server response code " + version
        raw_input("\n  Press Enter to exit...")
        sys.exit(1)
    except urllib2.URLError as e:
        print "\n  Cannot reach server. Try again later."
        print "  Reason: {0}".format(e.reason)
        raw_input("\n  Press Enter to exit...")
        sys.exit(1)

    if version is not None:
        return version.read()
    else:
        return None


# Creates a binary file that stores a packed integer which represents patch version
def create_version_file(path, version_int):
    if path is None or version_int is None:
        return False
    if not fileutils.dir_exists(path):
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

    if not fileutils.file_exists(version_path):
        return None

    with open(version_path, 'rb') as file_handle:
        version = struct.unpack('i', file_handle.read())[0]
        version_str = str(version)
        return version_str[0] + '.' + version_str[1] + '.' + version_str[2]


# Returns path to downloaded file
def download_file(download_url):
    print "\n  Requesting file download, please wait...",
    print "(this might take a while)\n"
    patch = urllib2.urlopen(download_url)
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
    print " Download complete:",
    print progress
    return getcwd() + "\\" + file_name


# Returns path to extracted file
def extract_zip(zip_path):
    print "\n  Extracting archive",
    print ".",
    zip_ref = zipfile.ZipFile(zip_path, 'r')
    print ".",
    output_dir = zip_path.split(".")[0]
    zip_ref.extractall(output_dir)
    print ".",
    print "\tdone"
    zip_ref.close()
    return output_dir


# Archives a directory into a zip file
def backup_zip(dst_path, src_path):
    if fileutils.dir_exists(dst_path) and fileutils.dir_exists(src_path):
        print "\n  Creating backup",
        date = time.strftime("%Y-%m-%d")
        print ".",
        backup_name = fileutils.get_dirname(src_path) + "_Backup_" + date
        print ".",
        shutil.make_archive(dst_path + "\\" + backup_name, 'zip', src_path)
        print ".",
        print "\tdone"


# Removes a list of files and directories
# Returns True if successful and False otherwise
def clean_up(path_list):
    print "\n  Cleaning up",

    if path_list is None:
        print ".",
        print ".",
        print ".",
        print "\t\tfailed"
        return False

    for path in path_list:
        if fileutils.dir_exists(path):
            fileutils.remove_dir_silent(path)
            continue
        if fileutils.file_exists(path):
            fileutils.remove_file_silent(path)
            print ".",
            print ".",
    print "\t\tdone"
    return True


def install_patch(dst_path, src_path):
    print "\n  Installing patch",
    if fileutils.dir_exists(src_path):
        print ".",
        fileutils.remove_dir_silent(dst_path)
        print ".",
        shutil.copytree(src_path, dst_path)
        print ".",
        print "\tdone"
    else:
        print ".",
        print ".",
        print ".",
        print "\tfailed"
        raw_input("\n  Press Enter to exit...")
        sys.exit(1)


def print_logo():
    print "  _____          _ _  ____                      "
    print " |_   _| __ ___ | | |/ ___| __ _ _ __ ___   ___ "
    print "   | || '__/ _ \| | | |  _ / _` | '_ ` _ \ / _ \\"
    print "   | || | | (_) | | | |_| | (_| | | | | | |  __/"
    print "   |_||_|  \___/|_|_|\____|\__,_|_| |_| |_|\___|"
    print "   _   _           _       _                    "
    print "  | | | |_ __   __| | __ _| |_ ___ _ __         "
    print "  | | | | '_ \ / _` |/ _` | __/ _ \ '__|        "
    print "  | |_| | |_) | (_| | (_| | ||  __/ |           "
    print "   \___/| .__/ \__,_|\__,_|\__\___|_|           "
    print "        |_|                                     "
    print "                                                "
    print "                              by LizardWizard   "
    print "\n\n"


print_logo()

PATCH_URL = "https://www.dropbox.com/s/accz9cxgxpkswhv/TG-NeoGK.zip?dl=1"
ADDON_COUGHS_URL = "https://community.troll-game.org/files/getdownload/604-coughs-addon/"
ADDON_MPTHEME_URL = "https://community.troll-game.org/files/getdownload/612-monty-phytons-theme-addon/"
ADDON_NI_URL = "https://community.troll-game.org/files/getdownload/602-trollgame-ni-addon/"
ADDON_BANNERS_URL = "https://community.troll-game.org/files/getdownload/826-trollgames-banners-addon/"
VERSION_URL = "http://troll-game.org/api/neogk/version"
WARBAND_PATH = get_warband_path()
MODULES_PATH = WARBAND_PATH + r"\Modules"
NATIVE_PATH = MODULES_PATH + r"\Native"
SOUNDS_PATH = NATIVE_PATH + r"\Sounds"
TEXTURES_PATH = NATIVE_PATH + r"\Textures"

# Warband installation not found
if WARBAND_PATH is None:
    print "  Warband not found."
    raw_input("\n  Press Enter to exit...")
    sys.exit(1)

print "  Connecting to server..."
LATEST_VERSION = check_latest_version(VERSION_URL)
system('cls')
print_logo()

# Warband installation found
print "  Warband found:     \t{0}\n".format(WARBAND_PATH)
print "  Latest version:    \t{0}\n".format(LATEST_VERSION)

# Patch not found
if patch_found(NATIVE_PATH) is False:
    print "  Installed version: \tnot found\n"
    print "\n  Would you like to install? (y/n)"
    while True:
        choice = raw_input("  > ")
        if choice.lower() == 'y':
            archive_path = download_file(PATCH_URL)
            archive_deflated_path = extract_zip(archive_path)
            backup_zip(MODULES_PATH, NATIVE_PATH)
            install_patch(NATIVE_PATH, archive_deflated_path + r"\TG-NeoGK\Native")
            create_version_file(NATIVE_PATH, version_to_int(LATEST_VERSION))
            clean_up([archive_deflated_path, archive_path])
            print "\n  TrollPatch installed successfully. Version: %s" % check_installed_version(NATIVE_PATH)
            break
        elif choice.lower() == 'n':
            print "  Bye."
            sys.exit(0)

    raw_input("\n  Press Enter to exit...")
    print "  Bye."
    sys.exit(0)

# Patch found
installed_version = check_installed_version(NATIVE_PATH)
print "  Installed version: \t%s\n" % installed_version

# Newer patch available
if installed_version < LATEST_VERSION:
    print "\n  Would you like to update? (y/n)"
    while True:
        choice = raw_input(" > ")
        if choice.lower() == 'y':
            archive_path = download_file(PATCH_URL)
            archive_deflated_path = extract_zip(archive_path)
            backup_zip(MODULES_PATH, NATIVE_PATH)
            install_patch(NATIVE_PATH, archive_deflated_path + r"\TG-NeoGK\Native")
            create_version_file(NATIVE_PATH, version_to_int(LATEST_VERSION))
            clean_up([archive_deflated_path, archive_path])
            print "\n  TrollPatch installed successfully. Version: %s" % check_installed_version(NATIVE_PATH)
            break
        elif choice.lower() == 'n':
            print "  Bye."
            sys.exit(0)
    raw_input("Press Enter to exit...")
    print "  Bye."
    sys.exit(0)

# Patch is up-to-date already
print "\n  Already up to date!\n"
raw_input("\n  Press Enter to exit...")
print "  Bye."
sys.exit(0)
