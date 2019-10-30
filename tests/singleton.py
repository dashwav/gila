import gila


def singleton_helper():
    key = "test"
    value = "new_value"
    gila.override(key, value)
