"""
This is the main file for the Gila library
"""
from typing import Any
from utils import deep_search
from os import path

_supported_exts = ["yaml", "yml"]
_key_delim = "."


class Gila():
    """
    An instance of the config store
    """
    def __init__(self):
        global _supported_exts
        global _key_delim
        self.__supported_exts = _supported_exts
        self.__key_delim = _key_delim
        self.__config_paths = []
        self.__config_name = None
        self.__config_type = None
        self.__config_file = None
        self.__env_prefix = None
        self.__allow_empty_env = True
        self.__aliases = {}
        self.__config = {}
        self.__defaults = {}
        self.__overrides = {}
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

    def __get_config_file(self):
        if not self.__config_file:
            self.__config_file = self.__find_config_file()
        return self.__config_file

    def __get_config_type(self):
        if not self.__config_type:
            filepath = self.__get_config_file()
            filename, file_extension = path.splitext(filepath)
            return file_extension
        return self.__config_type

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

    def __register_alias(self, alias: str, key: str):
        if alias == key or alias == self.__real_key(key):
            return
            # TODO: Error, circular reference
        found_config_val = self.__config[alias]
        if found_config_val:
            del self.__config[alias]
            self.__config[key] = found_config_val
        found_defaults_val = self.__defualts[alias]
        if found_defaults_val:
            del self.__defualts[alias]
            self.__defualts[key] = found_defaults_val
        found_override_val = self.__overrides[alias]
        if found_override_val:
            del self.__overrides[alias]
            self.__overrides[key] = found_override_val
        self.__aliases[alias] = key

    def __real_key(self, key: str):
        found_key = self.__aliases[key]
        if found_key:
            return self.__real_key(found_key)
        return key

    def in_config(self, key: str):
        return key in self.__config

    def set_default(self, key: str, value: Any):
        """
        Sets the default value for key to value
        """
        key = self.__real_key(key)

        path = key.split(self.__key_delim)
        last_key = path[-1]
        deepest_dict = deep_search(self.__defaults, path[0:-1])

        deepest_dict[last_key] = value

    def set(self, key: str, value: Any):
        """
        Sets the override value for key to value
        """
        key = self.__real_key(key)

        path = key.split(self.__key_delim)
        last_key = path[-1]
        deepest_dict = deep_search(self.__overrides, path[0:-1])

        deepest_dict[last_key] = value

    def read_in_config(self):
        """
        Will read in config from file
        """
        filename = self.__get_config_file()

        if self.__get_config_file not in self.__supported_exts:
            return
            # TODO: add config not supported error
        return filename
        # TODO: Read in file

    def __bind_env(self, key: str, env_key: str = None):
        if not key:
            return
            # TODO: add Error (Missing key to bind to)
        key = key.lower()
        if not env_key:
            env_key = self.__merge_with_env_prefix(key)
        self.__env[key] = env_key

    def __find(self, lower_key: str):

        # TODO: Overrides by set()
        # TODO: Command Flags
        # TODO: ENV Vars
        # TODO: Config File
        # TODO: Defaults
        return None

    # TODO: Add alias functionality
