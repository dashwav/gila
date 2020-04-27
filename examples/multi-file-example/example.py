"""Multi-file example.

This example code will show you how singleton instances operate.
"""
# Import module and prepend path
import gila  # noqa

# import secondary file, this file also imports gila
from misc import string_builder  # noqa


# define a new function
def print_welcome():
    print(string_builder("Test User"))


# now let's test setting defaults
gila.set_default("noun", "home")
gila.set_config_name("config")
gila.add_config_path('./')
gila.read_config_file()

"""Output:
Welcome to Hawaii, Test User
"""
print_welcome()

# So inside of the `misc.py` file, the singleton instance
#   is **NOT** segregated from the global instance.

# This is the basic principle of a singleton
# However, the module allows for more instantiation
# if you call the class directly.
# To be more explicit let's try something else.
# First reset the original singleton
gila.reset()

# now let's test setting defaults
g1 = gila.Gila()
g2 = gila.Gila()
g1.set_default("noun", "home")
g1.set_config_name("config")
g1.add_config_path('./')
g1.read_config_file()

"""Output:
Welcome to Hawaii, Test User
g1 is g2? False
"""
print_welcome()
print('g1 is g2?', g1 is g2)

# What is the use in this? Well users can have 2 separate configuration spaces
#   for security reasons. e.g. `g2` can hold all the secret tokens to be
#   passed to apps while `g1` holds the general configurations to be
#   accessible by the client.
