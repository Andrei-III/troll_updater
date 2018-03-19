class TrollAddon:
    """
    Class that encapsulates the name, download URL and version
    string representation of a TrollGame Addon
    """

    def __init__(self, name, url, version):
        self.__name = name
        self.__url = url
        self.__version = version

    def get_name(self):
        return self.__name

    def get_url(self):
        return self.__url

    def get_version(self):
        return self.__version

    def to_string(self):
        """
        A string representation of the object

        :return: The name and version of the patch
        as a string representation (e.g. Ni! v1.0).
        """
        return self.__name + ' v' + self.__version
