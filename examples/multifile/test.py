import gila
from utils import string_builder


def print_welcome():
    print(string_builder("Test User"))


gila.set_default("noun", "home")
gila.set_config_name("config")
gila.add_config_path('./')
gila.read_in_config()
print_welcome()
