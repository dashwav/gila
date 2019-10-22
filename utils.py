"""
Misc functions to clean up ain file
"""
from typing import List


def deep_search(haystack: dict, path: List[str]):
    """
    If path = ["foo", "bar", "baz"]
    The assumed values are:
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
    """
    if not isinstance(haystack, dict):
        raise TypeError()
    if not isinstance(path, list):
        raise TypeError()
    to_search = haystack
    for item in path:
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
