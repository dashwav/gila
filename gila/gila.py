"""
Gila is a python3 configuration library based very heavily on the
Viper_ config library for Go. It is designed to facilitate making
12Factor_ apps as easy as possible using python3.

You can either use the Gila library as a singleton pattern, by using

::

    import gila

    gila.get("key")

or you can create an instance to use in your application like this

::

    from gila import Gila

    gila_instance = Gila()
    gila_instance.get("key")

All functions of the gila class are available in the singleton instance
with the addition of ``gila.reset()``, which will reset the singleton
instance back to empty.

.. _Viper: https://github.com/spf13/viper
.. _12Factor: https://12factor.net/
"""
from typing import List, Any
from .util.errors import (ConfigNotSupported, ConfigFileNotFound,
                          CircularReference)
from .util.helpers import (deep_search, yaml_to_dict, prop_to_dict,
                           json_to_dict, toml_to_dict, hcl_to_dict,
                           dict_merge, env_to_dict)
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
_allowed_falsy_values = ([], (), {}, set(), '', range(0), 0, 0.0, 0j, False)

__all__ = [
    "ConfigNotSupported",
    "ConfigFileNotFound",
    "CircularReference",
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
    "unbind_env",
    "bind_env",
    "override_with_env",
    "register_alias",
    "deregister_alias",
    "override",
    "remove_override",
    "read_config_file",
    "get",
    "debug",
    "all_config"
]


class Gila():
    """
    An instance of the Gila config store
    """

    def __init__(self):
        self.reset()

    def reset(self):
        """
        Resets all of the values in the singleton instance of Gila
        """
        global _supported_exts
        global _key_delim
        self.__supported_exts = _supported_exts
        self.__key_delim = _key_delim
        self.__config_paths = []
        self.__automatic_env_applied = False
        self.__config_name = None
        self.__config_type = None
        self.__config_file = None
        self.__config_resolver = None
        self.__env_prefix = None
        self.__allow_empty_env = True
        self.__aliases = {}
        self.__config = {}
        self.__defaults = {}
        self.__overrides = {}
        self.__env = {}

    # Hidden methods for backend work, these are unexposed
    def __get_config_file(self):
        if not self.__config_file:
            self.__config_file = self.__find_config_file()
        return self.__config_file

    def __get_config_type(self):
        filepath = self.__get_config_file()
        _, file_extension = os_path.splitext(filepath)
        if file_extension != self.__config_type:
            self.__config_type = file_extension
            self.set_config_type(file_extension)
        return self.__config_type

    def __search_in_path(self, filepath: str):
        for ext in self.__supported_exts:
            if os_path.exists(os_path.join(
                    filepath, f'{self.__config_name}{ext}')):
                self.set_config_type(ext)
                return os_path.join(filepath, f'{self.__config_name}{ext}')
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

    def __merge_with_env_prefix(self, merge: str):
        if not self.__env_prefix:
            return merge.upper()
        return f'{self.__env_prefix.upper()}_{merge.upper()}'

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

    def __real_key(self, key: str):
        key = str(key)
        if key in self.__aliases:
            return self.__real_key(self.__aliases[key])
        return key

    def __is_path_shadowed_in_deep_dict(self, path: List[str], to_check: dict):
        parent_val = None
        for index, _ in enumerate(path):
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
        for index, _ in enumerate(path):
            parent_key = self.__key_delim.join(path[0:index])
            if parent_key in to_check:
                return parent_key
        return None

    def __is_path_shadowed_in_auto_env(self, path: List[str]):
        for index, _ in enumerate(path):
            parent_key = self.__key_delim.join(path[0:index])
            value = os_env.get(self.__merge_with_env_prefix(parent_key))
            if value:
                return parent_key
        return None

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
        if found_value or found_value in _allowed_falsy_values:
            return found_value
        path_shadow = self.__is_path_shadowed_in_flat_dict(
            path, self.__overrides)
        if nested and path_shadow:
            return None

        # Search ENV vars
        if self.__automatic_env_applied:
            value = os_env.get(self.__merge_with_env_prefix(key))
            if value or value in _allowed_falsy_values:
                return value
            path_shadow = self.__is_path_shadowed_in_auto_env(path)
            if nested and path_shadow:
                return None

        if key in self.__env:
            env_key = self.__env[key]
            value = os_env.get(env_key)
            if value or value in _allowed_falsy_values:
                return value
        path_shadow = self.__is_path_shadowed_in_flat_dict(path, self.__env)
        if nested and path_shadow:
            return None

        # Search Config vars
        value = self.__search_dict_with_prefix(self.__config, path)
        if value or value in _allowed_falsy_values:
            return value
        path_shadow = self.__is_path_shadowed_in_deep_dict(path, self.__config)
        if nested and path_shadow:
            return None

        value = self.__search_dict(self.__defaults, path)
        if value or value in _allowed_falsy_values:
            return value
        return None

    # These are the primary methods for retrieving values
    def get(self, key: str):
        """
        This fetches a value from the config store for a given key. Returns
        None if no value is found.

        The order of precedence on get is: overrides > environment variables
        > config vars > default values.

        :param key: :py:class:`str`: The key to search the config store for

        """
        return self.__find(key)

    def is_set(self, key: str):
        """
        Checks if a given key is in the config store.

        :param key: :py:class:`str`: Key to check

        """
        found_key = self.__find(key.lower())
        if found_key is not None:
            return True
        return False

    def all_config(self):
        """
        Returns a dictionary representing all of the current config values
        with the overrides in place.
        """
        _d1 = self.__overrides
        _t = None
        _d = [self.__env, self.__config, self.__defaults]
        for _d2 in _d:
            if _t is None:
                _t = dict_merge(_d1, _d2)
            else:
                _t = dict_merge(_t, _d2)
        _t = [self.__real_key(key) for key in _t]
        _t = dict([(key, self.__find(key)) for key in _t])
        return _t

    # For Debugging
    def debug(self):
        """
        Prints all of the instance internal dictionaries for debugging purposes
        """
        print(f'Aliases: {self.__aliases}\n')
        print(f'Override: {self.__overrides}\n')
        print(f'Env: {self.__env}\n')
        print(f'Config: {self.__config}\n')
        print(f'Defaults: {self.__defaults}\n')

    # Functions related to aliasing
    def register_alias(self, alias: str, key: str):
        """
        Registers an alias for a given key. When a key has an alias,
        gila.Get(key) and gila.Get(alias) will return the same value

        :param alias: :py:class:`str`: Alias to give key
        :param key: :py:class:`str`: Real key in the config store

        """
        if alias == key or alias == self.__real_key(key):
            raise CircularReference("No circular references")
        self.__aliases[alias] = key

    def deregister_alias(self, alias: str):
        """
        Removes an alias for a key in the config store.

        :param alias: :py:class:`str`: Alias to remove from config store
        """
        if alias in self.__aliases:
            del self.__aliases[alias]

    # Functions related to overrides
    def override(self, key: str, value: Any):
        """
        Sets the override value for a given key. Override values will take
        precedence over all other found values of a given key

        :param key: :py:class:`str`: The key in the config store
        :param value: Any: The override value to be set for the key

        """
        key = self.__real_key(key)
        path = key.split(self.__key_delim)
        last_key = path[-1]
        deepest_dict = deep_search(self.__overrides, path[0:-1])

        deepest_dict[last_key] = value

    def remove_override(self, key: str):
        """
        Removes the override for a key, if it is currently set

        :param key: :py:class:`str`: They key to remove the override for
        """
        key = self.__real_key(key)
        if key in self.__overrides:
            del self.__overrides[key]

    def override_with_env(self, prefix: str):
        """
        Finds all env vars with given prefix and sets them
        as overrides with a lowercase key. This would allow for a one-time
        load of environment vars to the config store. The loaded env vars will
        be loaded in as overrides, meaning they will take precedence over all
        other values

        :param prefix: :py:class:`str`: The prefix for Gila to use while
            searching.

        """
        for key, value in os_env.items():
            if key.startswith(prefix):
                self.override(key[len(prefix)+1:].lower(), value)

    # Functions related to env
    def automatic_env(self):
        """
        Tells Gila to automatically load env vars that
        start with the env_prefix, if set.
        """
        self.__automatic_env_applied = not self.__automatic_env_applied

    def set_env_prefix(self, prefix: str):
        """
        Sets the prefix that the automatic environment loader will use to find
        values for a given key. For instance, set_env_prefix("prefix") will
        set the prefix Gila is looking for to ``PREFIX_``. This means that when
        gila.get("key") is ran and automatic_env is enabled, Gila will look
        for the value in ``PREFIX_KEY``

        :param prefix: :py:class:`str`: The prefix to be added. This value
            will be uppercased and have "_" suffixed

        """
        if not prefix:
            return
        self.__env_prefix = prefix

    def bind_env(self, key: str, env_key: str = None):
        """
        Binds a given key to an environemnt variable. Default usage with
        bind_env(key) would bind the config value ``key`` with the environment
        value ``KEY``. If an env_key is passed in, it will be used instead of
        the default uppercased key. eg bind_env(key, env_key) will bind the
        config value of ``key`` to ``ENV_KEY``.

        NOTE: If env_key is not passed in, the key will be merged with a given
        prefix, should one exist.

        :param key: :py:class:`str`: Key to bind to
        :param env_key: :py:class:`str`:  (Default value = None) Optional
            env key to bind the config key to. If not present, fallback will
            be key.upper()

        """
        key = key.lower()
        if not env_key:
            env_key = self.__merge_with_env_prefix(key)
        self.__env[key] = env_key

    def unbind_env(self, key: str):
        """
        Removes a binding between an env_var and a key, if it exists

        :param key: :py:class:`key`
        """
        if key in self.__env:
            del self.__env[key]

    # Functions related to config file loading
    def set_config_type(self, filetype: str):
        """
        Sets the file extension that gila should look for -
        if not set, gila will look for a file with *any* of the
        supported filetypes.

        :param filetype: :py:class:`str`: The extension of the
            config file that Gila should look for

        """
        if not filetype:
            return
        if filetype not in self.__supported_exts:
            raise ConfigNotSupported(
                f"The extensions Gila supports are {self.__supported_exts}")
        if filetype in ['.yaml', '.yml']:
            self.__config_type = '.yaml'
            self.__config_resolver = yaml_to_dict
        elif filetype in ['.toml']:
            self.__config_type = '.toml'
            self.__config_resolver = toml_to_dict
        elif filetype in ['.json']:
            self.__config_type = '.json'
            self.__config_resolver = json_to_dict
        elif filetype in ['.hcl']:
            self.__config_type = '.hcl'
            self.__config_resolver = hcl_to_dict
        elif filetype in ['.properties', '.props', '.prop']:
            self.__config_type = '.properties'
            self.__config_resolver = prop_to_dict
        elif filetype in ['.env']:
            self.__config_type = '.env'
            self.__config_resolver = env_to_dict

    def set_config_name(self, filename: str):
        """
        Sets the filename that Gila will look for. If the filename is
        set and the config type is not, Gila will search for a config
        file with the given config name and **any** of the supported
        extensions

        :param filename: :py:class:`str`: The name of the
            config file that Gila should look for

        """
        if not filename:
            return
        self.__config_name = filename

    def add_config_path(self, filepath: str):
        """
        Adds a filepath to the list of filepaths to search for config files
        The filepath can be either an absolute path or a path relative to the
        current working directory

        :param filepath: :py:class:`str`: The filepath to be added

        """
        if not filepath:
            return
        self.__config_paths.append(filepath)

    def set_config_file(self, filepath: str):
        """
        Sets the filepath to the intended config file. This is an increased
        level of verbosity than set_config_name and set_config_type, as if
        the config file is set, Gila will only look for the config file in
        that one location.

        :param filepath: :py:class:`str`: The filepath to the intended config
            file

        """
        if not filepath:
            return
        self.__config_file = filepath
        self.__get_config_type()

    def read_config_file(self):
        """
        Will read in config from file. Gila will iterate through the given
        filepaths, and return the first file found in a config path that has
        the extension that is set with gila.set_config_type() if it is set, or
        the first file with a supported filetype.
        """
        filename = self.__get_config_file()
        config = self.__config_resolver(filename)
        if config is None:
            config = {}
        if not config:
            raise ConfigFileNotFound(
                f"Couldn't find config {filename}")
        self.__config = dict_merge(config, self.__config)

    def in_config(self, key: str):
        """
        Checks if a given key is found in the config file provided. Returns
        false if no file has been loaded in yet

        :param key: :py:class:`str`: key to check in config values

        """
        return key in self.__config

    # Functions related to default values
    def set_default(self, key: str, value: Any):
        """
        Sets the default value for key to value. If no other values are
        found when running gila.get(key), the default value will be returned.

        :param key: :py:class:`str`: The real key in the config store
        :param value: Any: The default value to be set for the key

        """
        path = key.split(self.__key_delim)
        last_key = path[-1]
        deepest_dict = deep_search(self.__defaults, path[0:-1])

        deepest_dict[last_key] = value

    def remove_default(self, key: str):
        """
        Remove the default key.

        :param key: :py:class:`str`: The real key in the config store

        """
        path = key.split(self.__key_delim)
        last_key = path[-1]
        deepest_dict = deep_search(self.__defaults, path[0:-1])

        del deepest_dict[last_key]


# Singleton functionality
_gila = Gila()


def reset():
    # Singleton function for Gila.reset
    _gila.reset()


def all_config():
    # Singleton function for Gila.all_config
    return _gila.all_config()


def automatic_env():
    # Singleton function for Gila.automatic_env
    return _gila.automatic_env()


def set_config_type(filetype: str):
    # Singleton function for Gila.set_config_type
    return _gila.set_config_file(filetype)


def set_config_name(filename: str):
    # Singleton function for Gila.set_config_name
    return _gila.set_config_name(filename)


def set_config_file(filepath: str):
    # Singleton function for Gila.set_config_file
    return _gila.set_config_file(filepath)


def add_config_path(filepath: str):
    # Singleton function for Gila.add_config_path
    return _gila.add_config_path(filepath)


def set_env_prefix(prefix: str):
    # Singleton function for Gila.set_env_prefix
    return _gila.set_env_prefix(prefix)


def is_set(key: str):
    # Singleton function for Gila.is_set
    return _gila.is_set(key)


def in_config(key: str):
    # Singleton function for Gila.in_config
    return _gila.in_config(key)


def set_default(key: str, value: Any):
    # Singleton function for Gila.set_default
    return _gila.set_default(key, value)


def remove_default(key: str):
    # Singleton function for Gila.remove_default
    return _gila.remove_default(key)


def bind_env(key: str, env_key: str = None):
    # Singleton function for Gila.bind_env
    return _gila.bind_env(key, env_key)


def unbind_env(key: str):
    # Singleton function for Gila.unbind_env
    return _gila.unbind_env(key)


def override_with_env(prefix: str):
    # Singleton function for Gila.override_with_env
    return _gila.override_with_env(prefix)


def register_alias(alias: str, key: str):
    # Singleton function for Gila.register_alias
    return _gila.register_alias(alias, key)


def deregister_alias(alias: str):
    # Singleton function for Gila.deregister_alias
    return _gila.deregister_alias(alias)


def override(key: str, value: Any):
    # Singleton function for Gila.override
    return _gila.override(key, value)


def remove_override(key: str):
    # Singleton function for Gila.remove_override
    return _gila.remove_override(key)


def read_config_file():
    # Singleton function for Gila.read_config_file
    return _gila.read_config_file()


def get(key: str):
    # Singleton function for Gila.get
    return _gila.get(key)


def debug():
    # Singleton function for Gila.debug
    _gila.debug()
