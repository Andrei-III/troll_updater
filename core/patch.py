class TrollPatch:
    """
    Class that encapsulates a download URL for the TrollGame Patch
    and a version string representation.
    """

    NAME = "TrollGame Patch"

    def __init__(self, url, version):
        self.__url = url
        self.__version = version

    def get_url(self):
        return self.__url

    def get_version(self):
        return self.__version
