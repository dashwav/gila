"""
Misc functions to clean up main file
"""
from typing import List
from yaml import safe_load
from json import load as json_load
from toml import load as toml_load
from hcl import load as hcl_load
from dotenv import dotenv_values as env_load
from configparser import ConfigParser


def deep_search(haystack: dict, keypath: List[str]):
    """
    If path = ["foo", "bar", "baz"]
    The assumed values are:
    ::

        haystack = {
            foo: {
                bar: {
                    baz: {}
                }
            }
        }

    Where the dict that baz points to is returned

    If this is not the case, the config haystack is modified
    in order to facilitate this

    :param haystack: :py:class:`dict` - dictionary to search

    :param keypath: :py:class:`~typing.List[str]` - path to follow while
        searching
    """
    if not isinstance(haystack, dict):
        raise TypeError()
    if not isinstance(keypath, list):
        raise TypeError()
    to_search = haystack
    for item in keypath:
        if item not in to_search:
            # to_search[item] is not set, create dict and continue
            to_search[item] = {}
            to_search = to_search[item]
            continue
        intermediary = to_search[item]
        if not isinstance(intermediary, dict):
            # Intermediary is a value, replace with a dict
            del to_search[item]
            to_search[item] = {}
        to_search = to_search[item]
    return to_search


def yaml_to_dict(filepath: str):
    """
    Loads in config from a yaml file to a dictionary using
    pyyaml_

    .. _pyyaml: https://github.com/yaml/pyyaml

    :params filepath: :py:class:`str` - Filepath to
        yaml config file to unmarshal
    """
    try:
        with open(filepath, 'r') as yml_config:
            return safe_load(yml_config)
    except Exception:
        return None


def prop_to_dict(filepath: str):
    """
    Loads in config from a dotenv file to a dictionary using
    the configparser stdlib

    NOTE: All values read in as strings.

    :params filepath: :py:class:`str` - Filepath to
        dotenv config file to unmarshal
    """
    try:
        with open(filepath, 'r') as prop_config:
            config = ConfigParser()
            config.read_string(
                '[config]\n' + prop_config.read())
            return dict(config.items('config'))
    except Exception:
        return None


def json_to_dict(filepath: str):
    """
    Loads in config from a json file to a dictionary using
    json stlib

    :params filepath: :py:class:`str` - Filepath to
        json config file to unmarshal
    """
    try:
        with open(filepath, 'r') as json_config:
            return json_load(json_config)
    except Exception:
        return None


def toml_to_dict(filepath: str):
    """
    Loads in config from a toml file to a dictionary using
    toml_

    .. _toml: https://github.com/uiri/toml

    :params filepath: :py:class:`str` - Filepath to
        toml config file to unmarshal
    """
    try:
        with open(filepath, 'r') as toml_config:
            return toml_load(toml_config)
    except Exception:
        return None


def hcl_to_dict(filepath: str):
    """
    Loads in config from an hcl file to a dictionary using
    pyhcl_

    .. _pyhcl: https://github.com/virtuald/pyhcl

    :params filepath: :py:class:`str` - Filepath to
        hcl config file to unmarshal
    """
    try:
        with open(filepath, 'r') as hcl_config:
            return hcl_load(hcl_config)
    except Exception:
        return None


def env_to_dict(filepath: str):
    """
    Loads in config from a dotenv file to a dictionary using
    dotenv_

    .. _dotenv: https://github.com/theskumar/python-dotenv

    NOTE: All values read in as strings.

    :params filepath: :py:class:`str` - Filepath to
        dotenv config file to unmarshal
    """
    try:
        config = env_load(filepath)
        return config
    except Exception:
        return None


def dict_merge(dict_1: dict, dict_2: dict):
    """Merge two dictionaries.

    `dict_1` > `dict_2`
    Works by creating set of all keys between two dictionaries.
    Then iterates through and gathers values from first dict_1
    if present, else falls back to dict_2.

    :params dict_1: the primary dictionary to pull results from
    :params dict_2: the secondary dictionary to pull results from
    """
    keys = [key for key in set().union(dict_1, dict_2)]
    return dict((key, dict_1.get(key) or dict_2.get(key))
                for key in keys)
