import struct

from core import os_utils

# GLOBALS
VERSION_FILE_EXT = ".version"


class Version:
    """
    Class to facilitate working with versions.
    """

    def __init__(self, major, minor, build):
        self.__major = major
        self.__minor = minor
        self.__build = build

    def to_str(self):
        return str(self.__major) + '.' + \
               str(self.__minor) + '.' + \
               str(self.__build)

    def to_int(self):
        """
        Builds an integer representation of the version
        from 3 separate parts: major release number,
        minor release number and build release number.
        The format will be [major][minor][build].

        :return: The parsed integer value of the given string
        """
        return int((str(self.__major) +
                    str(self.__minor) +
                    str(self.__build)))

    def save_to_file(self, dir_path, file_name):
        """
        Creates a troll-game version file (binary)
        that stores a packed integer which represents a version

        :param file_name: The name of the version file to be created (excluding extension).
        :param dir_path: The absolute path of the directory where the file will be written.
        :return: True if the operation was successful or False otherwise.
        """
        if dir_path is None:
            return False
        if not os_utils.dir_exists(dir_path):
            return False
        if self.to_int() < 0:
            return False
        absolute_path = dir_path + '\\' + file_name + VERSION_FILE_EXT
        version_file = open(absolute_path, 'wb')
        version_file.write(struct.pack('i', self.to_int()))
        version_file.close()
        return True

    def equals(self, other):
        """
        Checks if this Version object is equal to the given Version object.

        :param other: A Version object to be compared with.
        :return: True if this Version object has the same contents
        as the other Version object and False otherwise.
        """
        if not other:
            return False
        if not isinstance(other, Version):
            return False
        return self.__major == other.__major and \
               self.__minor == other.__minor and \
               self.__build == other.__build

    def compare_to(self, other):
        """
        Checks if this Version object is greater, lesser or equal
        to the given Version object.

        :param other: A Version object to be compared with.
        :return: -1 if this object is lesser than the argument.
        0 if this object is equal to the argument.
        1 if this object is greater than the argument.
        :raise: ValueError if the given argument is not of type Version
        """
        if not isinstance(other, Version):
            raise ValueError("Given argument (type " + type(other) + ") is not of type Version.")

        if self == other or self.equals(other):
            return 0

        if self.__major > other.__major:
            return 1

        if self.__major < other.__major:
            return -1

        if self.__minor > other.__minor:
            return 1

        if self.__minor < other.__minor:
            return -1

        if self.__build > other.__build:
            return 1

        return -1  # At this point it's clear that the other is greater

    @staticmethod
    def read_version_file(file_path):
        """
        Reads the version from a trollgame version file.

        :param file_path: The absolute path to the version file.
        :return: The read version representation in string format (e.g. "1.2.1")
        or None if the file path is None / malformed or the file does not exist
        """
        if file_path is None:
            return None

        if not isinstance(file_path, (basestring, str, unicode)):
            return None

        if not os_utils.file_exists(file_path):
            return None

        with open(file_path, 'rb') as file_handle:
            version = struct.unpack('i', file_handle.read())[0]
            version_str = str(version)
            return version_str[0] + '.' + version_str[1] + '.' + version_str[2]

    @staticmethod
    def from_str(version_str):
        """
        Converts the given string version representation
        into a Version object.

        :param version_str: The string version representation to be converted.
        :return: A Version object or None if the
        string version representation is None, not an instance of
        one of :type:basestring, :type:str or :type:unicode or
        has an invalid format (a valid format is "1.0.0")
        """
        if not version_str:
            return None

        if not isinstance(version_str, (basestring, str, unicode)):
            return None

        version_tokens = version_str.split(".")

        if len(version_tokens) != 3:
            return None

        return Version(major=int(version_tokens[0]),
                       minor=int(version_tokens[1]),
                       build=int(version_tokens[2]))

    @staticmethod
    def from_file(file_path):
        """
        Reads and returns a string version representation
        from a troll-game version file.

        :param file_path: The absolute path to the version file.
        :return: A Version object containing the version read from the file
        or None if the file path is None/invalid or the file path does not exist.
        """
        if file_path is None:
            return None

        if not isinstance(file_path, (basestring, str, unicode)):
            return None

        if not os_utils.file_exists(file_path):
            return None

        with open(file_path, 'rb') as file_handle:
            version = struct.unpack('i', file_handle.read())[0]
            version_str = str(version)
            return Version(major=int(version_str[0]),
                           minor=int(version_str[1]),
                           build=int(version_str[2]))
