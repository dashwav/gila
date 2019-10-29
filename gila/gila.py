"""
This is the main file for the Gila library
"""
from typing import List, Any
from .util.errors import ConfigNotSupported, ConfigFileNotFound
from .util.errors import CircularReference
from .util.helpers import deep_search, yaml_to_dict, prop_to_dict
from .util.helpers import json_to_dict, toml_to_dict, hcl_to_dict
from .util.helpers import env_to_dict
from os import path as os_path
from os import environ as os_env

_supported_exts = [
    ".yaml", ".yml",
    ".toml",
    ".json",
    ".hcl",
    ".properties", ".props", ".prop",
    ".env",
    ]
_key_delim = "."

__all__ = [
    "Gila",
    "reset",
    "automatic_env",
    "set_config_type",
    "set_config_name",
    "set_config_file",
    "add_config_path",
    "set_env_prefix",
    "is_set",
    "in_config",
    "set_default",
    "bind_env",
    "register_alias",
    "set",
    "read_in_config",
    "get",
    "debug"
]


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
        self.__automatic_env_applied = False
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

    def automatic_env(self):
        self.__automatic_env_applied = True

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
            filename, file_extension = os_path.splitext(filepath)
            return file_extension
        return self.__config_type

    def add_config_path(self, filepath: str):
        if not filepath:
            return
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
            if os_path.exists(os_path.join(
                    filepath, f'{self.__config_name}{ext}')):
                return os_path.join(filepath, f'{self.__config_name}{ext}')
        return None

    def __search_dict(self, to_search: dict, path: List[str]):
        # End case
        if len(path) == 0:
            return to_search
        if path[0] in to_search:
            # Fast return
            if len(path) == 1:
                return to_search[path[0]]

            # Continue
            if isinstance(to_search[path[0]], dict):
                return self.__search_dict(to_search[path[0]], path[1:])

            # Value received, dict expected
            return None

    # TODO: swap position of arguments to match other functions
    def __search_dict_with_prefix(self, to_search: dict, path: List[str]):
        if len(path) == 0:
            return to_search

        for index in range(len(path), 0, -1):
            value = None
            delim = self.__key_delim
            key_prefix = delim.join(path[0:index])

            if key_prefix in to_search:
                if index == len(path):
                    return to_search[key_prefix]
                if isinstance(to_search[key_prefix], dict):
                    value = self.__search_dict_with_prefix(
                        to_search[key_prefix], path[index:])
                if value:
                    return value
        return None

    def __find_config_file(self):
        found_config = None
        for config_path in self.__config_paths:
            found_config = self.__search_in_path(config_path)
            if found_config:
                return found_config
        if not found_config:
            raise ConfigFileNotFound(
                f"Couldn't find config on paths: {self.__config_paths}")

    def is_set(self, key: str):
        found_key = self.__find(key.lower())
        if found_key is not None:
            return True
        return False

    def register_alias(self, alias: str, key: str):
        if alias == key or alias == self.__real_key(key):
            raise CircularReference("No circular references")
        found_config_val = None
        if alias in self.__config:
            found_config_val = self.__config[alias]
        if found_config_val:
            del self.__config[alias]
            self.__config[key] = found_config_val
        found_defaults_val = None
        if alias in self.__defaults:
            found_defaults_val = self.__defualts[alias]
        if found_defaults_val:
            del self.__defualts[alias]
            self.__defualts[key] = found_defaults_val
        found_override_val = None
        if alias in self.__overrides:
            found_override_val = self.__overrides[alias]
        if found_override_val:
            del self.__overrides[alias]
            self.__overrides[key] = found_override_val
        self.__aliases[alias] = key

    def __real_key(self, key: str):
        found_key = None
        if key in self.__aliases:
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
        config_type = self.__get_config_type()
        if config_type not in self.__supported_exts:
            raise ConfigNotSupported(
                f"The extensions Gila supports are {self.__supported_exts}")
        if config_type in ['.yaml', '.yml']:
            config = yaml_to_dict(filename)
        elif config_type in ['.toml']:
            config = toml_to_dict(filename)
        elif config_type in ['.json']:
            config = json_to_dict(filename)
        elif config_type in ['.hcl']:
            config = hcl_to_dict(filename)
        elif config_type in ['.properties', '.props', '.prop']:
            config = prop_to_dict(filename)
        elif config_type in ['.env']:
            config = env_to_dict(filename)
        else:
            config = {}
        self.__config = config

    def __is_path_shadowed_in_deep_dict(self, path: List[str], to_check: dict):
        parent_val = None
        for index, item in enumerate(path):
            parent_val = self.__search_dict(to_check, path[0:index])
            if not parent_val:
                return None
            if isinstance(parent_val, dict):
                continue
            return self.__key_delim.join(path[0:index])
        return None

    def __is_path_shadowed_in_flat_dict(self, path: List[str], to_check: Any):
        if not isinstance(to_check, dict):
            return None
        for index, item in enumerate(path):
            parent_key = self.__key_delim.join(path[0:index])
            if parent_key in to_check:
                return parent_key
        return None

    def __is_path_shadowed_in_auto_env(self, path: List[str]):
        for index, item in enumerate(path):
            parent_key = self.__key_delim.join(path[0:index])
            value = os_env.get(self.__merge_with_env_prefix(parent_key))
            if value:
                return parent_key
        return None

    def bind_env(self, key: str, env_key: str = None):
        key = key.lower()
        if not env_key:
            env_key = self.__merge_with_env_prefix(key)
        self.__env[key] = env_key

    def get(self, key: str):
        return self.__find(key)

    def __find(self, key: str):
        found_value = None
        path = key.split(self.__key_delim)
        nested = len(path) > 1

        path_shadow = self.__is_path_shadowed_in_deep_dict(
            path, self.__aliases)
        if nested and path_shadow:
            return None

        # Get real_key from aliases
        key = self.__real_key(key)
        path = key.split(self.__key_delim)
        nested = len(path) > 1

        # Search overrides
        found_value = self.__search_dict(self.__overrides, path)
        if found_value or found_value in [False]:
            return found_value
        path_shadow = self.__is_path_shadowed_in_flat_dict(
            path, self.__overrides)
        if nested and path_shadow:
            return None

        # TODO: Command Flags
        # Are command flags even going to be possible easily?

        # Search ENV vars
        if self.__automatic_env_applied:
            value = os_env.get(self.__merge_with_env_prefix(key))
            if value or value in [False]:
                return value
            path_shadow = self.__is_path_shadowed_in_auto_env(path)
            if nested and path_shadow:
                return None

        if key in self.__env:
            env_key = self.__env[key]
            value = os_env.get(env_key)
            if value or value in [False]:
                return value
        path_shadow = self.__is_path_shadowed_in_flat_dict(path, self.__env)
        if nested and path_shadow:
            return None

        # Search Config vars
        value = self.__search_dict_with_prefix(self.__config, path)
        if value or value in [False]:
            return value
        path_shadow = self.__is_path_shadowed_in_deep_dict(path, self.__config)
        if nested and path_shadow:
            return None

        value = self.__search_dict(self.__defaults, path)
        if value or value in [False]:
            return value
        return None

    def debug(self):
        print(f'Aliases: {self.__aliases}\n')
        print(f'Override: {self.__overrides}\n')
        print(f'Env: {self.__env}\n')
        print(f'Config: {self.__config}\n')
        print(f'Defaults: {self.__defaults}\n')


"""
Singleton functionality
"""

_gila = Gila()


def reset():
    global _gila
    _gila = Gila()


def automatic_env():
    return _gila.automatic_env()


def set_config_type(filetype: str):
    return _gila.set_config_file(filetype)


def set_config_name(filename: str):
    return _gila.set_config_name(filename)


def set_config_file(filepath: str):
    return _gila.set_config_file(filepath)


def add_config_path(filepath: str):
    return _gila.add_config_path(filepath)


def set_env_prefix(prefix: str):
    return _gila.set_env_prefix(prefix)


def is_set(key: str):
    return _gila.is_set(key)


def in_config(key: str):
    return _gila.in_config(key)


def set_default(key: str, value: Any):
    return _gila.set_default(key, value)


def bind_env(key: str, env_key: str = None):
    return _gila.bind_env(key, env_key)


def register_alias(alias: str, key: str):
    return _gila.register_alias(alias, key)


def set(key: str, value: Any):
    return _gila.set(key, value)


def read_in_config():
    return _gila.read_in_config()


def get(key: str):
    return _gila.get(key)


def debug():
    return _gila.debug()
