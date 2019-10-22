"""
This is the main file for the Gila library
"""
from os import path

_supported_exts = ["yaml", "yml"]


class Gila():
    """
    An instance of the config store
    """
    def __init__(self):
        global _supported_exts
        self.__supported_exts = _supported_exts
        self.__config_paths = []
        self.__config_name = None
        self.__config_type = None
        self.__config_file = None
        self.__env_prefix = None
        self.__allow_empty_env = True
        self.__config = {}
        self.__defaults = {}
        self.__env = {}

    def set_config_type(self, filetype: str):
        if not filetype:
            return
        self.__config_type = filetype

    def set_config_name(self, filename: str):
        if not filename:
            return
        self.__config_name = filename

    def set_config_file(self, filepath: str):
        if not filepath:
            return
        self.__config_file = filepath

    def add_config_path(self, filepath: str):
        if not filepath:
            return
        # TODO: Check if absPath is needed here
        self.__config_paths.append(filepath)

    def set_env_prefix(self, prefix: str):
        if not prefix:
            return
        self.__env_prefix = prefix

    def __merge_with_env_prefix(self, merge: str):
        if not self.__env_prefix:
            return merge.upper()
        return f'{self.__env_prefix.upper()}_{merge.upper()}'

    def __get_config_file(self):
        if not self.__config_file:
            self.__config_file = self.__find_config_file()
        return self.__config_file

    def __search_in_path(self, filepath: str):
        for ext in self.__supported_exts:
            if path.exists(path.join(filepath, f'{self.__config_name}.{ext}')):
                return path.join(filepath, f'{self.__config_name}.{ext}')
        return None

    def __find_config_file(self):
        found_config = None
        for config_path in self.__config_paths:
            found_config = self.__search_in_path(config_path)
            if found_config:
                return found_config
        if not found_config:
            # TODO: Add config not found exception
            return

    def is_set(self, key: str):
        found_key = self.__find(key.lower())
        if found_key is not None:
            return True
        return False

    def __find(self, lower_key: str):

        # TODO: Overrides by set()
        # TODO: Command Flags
        # TODO: ENV Vars
        # TODO: Config File
        # TODO: Defaults
        return None

    # TODO: Add alias functionality