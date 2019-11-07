import gila


def string_builder(to_insert: str):
    """
    Inserts a given string into a preformated string
    """
    config_var = gila.get("noun")
    return f'Welcome to {config_var}, {to_insert}'
