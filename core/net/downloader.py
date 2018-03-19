import os
import urllib2

from ui.ui_constants import *
from ui.ui_utils import print_indented


def get_file(download_url):
    """
    Downloads a file from specified URL
    while also printing the progress.

    :param download_url: The URL source of the file.
    :return: Absolute path to the downloaded file
    (which is current working directory with the filename)
    or None if the download failed.
    """
    patch = urllib2.urlopen(download_url)
    meta = patch.info()
    file_name = str(meta.getheaders("content-disposition")[0].split(';')[1].split("\"")[1])
    file_size = long(meta.getheaders("Content-Length")[0])
    filewriter = open(file_name, 'wb')
    print INDENTATION, "Downloading: %s  [ %s B ]" % (file_name, file_size)

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
            progress = INDENTATION + r"%10d [%3.2f%%]" % (downloaded_bytes, downloaded_bytes * 100. / file_size)
            progress = progress + chr(8) * (len(progress) + 1)
            print progress,

    filewriter.close()
    print_indented("Download complete:" + progress)
    return os.getcwd() + "\\" + file_name


def get_json(url):
    """
    Downloads a json from the given URL.

    :param url: The URL source of the json.
    :return:Returns the downloaded json or None
    if URL is malformed, the server is unreachable
    or the server fails to fulfill the request.
    """
    header = {
        'User-Agent': 'Mozilla/5.0 (X11 Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 '
                      'Safari/537.11',
        'Accept': 'text/html',
        'Accept-Charset': 'ISO-8859-1,utf-8q=0.7,*q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,enq=0.8',
        'Connection': 'close'}

    request = urllib2.Request(url, headers=header)
    version = urllib2.urlopen(request)
    return version.read() if version is not None else None
