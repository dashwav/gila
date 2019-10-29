"""
This will contain the custom errors Gila uses
"""


class ConfigNotSupported(Exception):
    pass


class ConfigFileNotFound(Exception):
    pass


class CircularReference(Exception):
    pass
