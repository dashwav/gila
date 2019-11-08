"""Misc supporting file."""

import gila


def string_builder(to_insert: str):
    """Insert a given string into a preformated string."""
    config_var = gila.get("noun")
    if config_var:
        return f'Welcome to {config_var}, {to_insert}'
    return f'Welcome to [HOME NOT SET], {to_insert}'
