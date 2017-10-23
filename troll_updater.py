import os
import urllib2
import zipfile
import shutil
import struct
import time
from _winreg import *


def dir_exists(dir_path):
	return os.path.isdir(dir_path);


def file_exists(file_path):
	return os.path.exists(file_path);


def get_warband_path():
	try:
		aKey = OpenKey(HKEY_LOCAL_MACHINE, r"SOFTWARE\mount&blade warband")
		install_path = QueryValueEx(aKey, "install_path")
		CloseKey(aKey)
		return install_path[0]
	except WindowsError:
		return None


def patch_found(native_path):
	if dir_exists(native_path):
		if file_exists(native_path + r'\version'):
			return True
		else:
			return False
	else:
		return False


def check_latest_version():
	header = {
		'User-Agent': 'Mozilla/5.0 (X11 Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
		'Accept': 'text/html',
       	'Accept-Charset': 'ISO-8859-1,utf-8q=0.7,*q=0.3',
       	'Accept-Encoding': 'none',
       	'Accept-Language': 'en-US,enq=0.8',
       	'Connection': 'close'}

	request = urllib2.Request("http://troll-game.org/api/neogk/version", headers=header)
	try:
		version = urllib2.urlopen(request)
	except:
		print "\n  Cannot reach server. Try again later."
		raw_input("  Press Enter to exit...")
		exit()

	return version.read()


def create_version_file(native_path, version):
	if dir_exists(native_path):
		version_file = open(native_path + r'\version', 'wb')
		version_file.write(struct.pack('i', version))
		version_file.close()


def version_to_int(version_str):
	if version_str != None:
		version_tokens = version_str.split('.')
		version = ""
		for token in version_tokens:
			version += token
		return int(version)

def check_installed_version(native_path):
	version_path = native_path + r'\version'
	if file_exists(version_path):
		with open(version_path, 'rb') as file_handle:
		    version = struct.unpack('i', file_handle.read())[0]
		    version_str = str(version)
		    return version_str[0] + '.' + version_str[1] + '.' + version_str[2]


def download_patch(patch_url):
	print "\n  Requesting file download, please wait...",
	file_name = patch_url.split('/')[-1].split('?')[0]
	print "(this might take a while)\n"
	patch = urllib2.urlopen(patch_url)
	filewriter = open(file_name, 'wb')
	meta = patch.info()
	file_size = int(meta.getheaders("Content-Length")[0])
	print "  Downloading: %s  [ %s B ]" % (file_name, file_size)

	downloaded_bytes = 0
	block_sz = 8192
	progress = "%10d [%3.2f%%]" % (downloaded_bytes, downloaded_bytes * 100. / file_size)

	while True:
		buffer = patch.read(block_sz)

		if not buffer:
			break
		else:
			downloaded_bytes += len(buffer)
			filewriter.write(buffer)
			progress = r"%10d [%3.2f%%]" % (downloaded_bytes, downloaded_bytes * 100. / file_size)
			progress = progress + chr(8)*(len(progress)+1)
			print progress,


	print " Download complete:",
	print progress
	filewriter.close() 
	return os.getcwd() + "\\" + file_name


def extract_zip(file_path):
	print "\n  Extracting archive...",
	zip_ref = zipfile.ZipFile(file_path, 'r')
	zip_ref.extractall("")
	print "done";
	zip_ref.close()
	return os.getcwd() + r"\TG-NeoGK"


def backup_zip(dst_path, src_path):
	if dir_exists(dst_path) and dir_exists(src_path):
		print "\n  Creating backup...",
		date = time.strftime("%Y-%m-%d")
		backup_name = r"\Native_Backup_" + date
		shutil.make_archive(dst_path + backup_name, 'zip', src_path)
		print "done";

def install_patch(dst_path, src_path):
	print "\n  Installing patch...",
	if dir_exists(src_path):
		remove_dir(dst_path)
		shutil.copytree(src_path, dst_path)
		print "done";
	else:
		print "failed";
		raw_input("\n  Press Enter to exit...")
		exit()


def remove_file(file_path):
	if file_exists(file_path):
		os.remove(file_path)


def remove_dir(dir_path):
	if dir_exists(dir_path):
		shutil.rmtree(dir_path, ignore_errors=True)


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


patch_url = "https://www.dropbox.com/s/5hdyljaz2zfui23/TG-NeoGKLatest.zip?dl=1"
warband_path = get_warband_path()
modules_path = warband_path + r"\Modules"
native_path = warband_path + r"\Modules\Native"
latest_version = check_latest_version()


if warband_path:
	print "  Warband found:     \t%s\n" % warband_path
	print "  Latest version:    \t%s\n" % latest_version

	if patch_found(native_path):
		installed_version = check_installed_version(native_path)
		print "  Installed version: \t%s\n" % installed_version
		if installed_version == latest_version:
			print "\n  Already up to date!\n"
			raw_input("\n  Press Enter to exit...")
			exit()
		elif installed_version < latest_version:
			print "\n  Would you like to update? (y/n)"
			while True:
				choice = raw_input("  > ")
				if choice.lower() == 'y':
					archive_path = download_patch(patch_url)
					archive_deflated_path = extract_zip(archive_path)
					backup_zip(modules_path, native_path)
					install_patch(native_path, archive_deflated_path + r"\Native")
					create_version_file(native_path, version_to_int(latest_version))
					print "\n  Cleaning up...",
					remove_dir(archive_deflated_path);
					remove_file(archive_path);
					print "done";
					print "\n  TrollPatch installed successfully. Version: %s" % check_installed_version(native_path)
					break
				elif choice.lower() == 'n':
					exit()
			raw_input("\n  Press Enter to exit...")
			exit()
	else:
		print "  Installed version: \tnot found\n"
		print "\n  Would you like to install? (y/n)"
		while True:
			choice = raw_input("  > ")
			if choice.lower() == 'y':
				archive_path = download_patch(patch_url)
				archive_deflated_path = extract_zip(archive_path)
				backup_zip(modules_path, native_path)
				install_patch(native_path, archive_deflated_path + r"\Native")
				create_version_file(native_path, version_to_int(latest_version))
				print "\n  Cleaning up...",
				remove_dir(archive_deflated_path);
				remove_file(archive_path);
				print "done";
				print "\n  TrollPatch installed successfully. Version: %s" % check_installed_version(native_path)
				break
			elif choice.lower() == 'n':
				exit()
		raw_input("\n  Press Enter to exit...")
		exit()
else:
	print "  Warband not found."
	raw_input("\n  Press Enter to exit...")
	exit()