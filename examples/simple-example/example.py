"""Simple example file.

This example code will show you the basic functionality of gila.
This showcases the common usecases: default values, reading from the
    environment, and retrieving values.
"""
import os
import gila  # noqa

# Setting default values for keys
gila.set_default('host', 'localhost:8080')
gila.set_default('allow_insecure', False)

# This will tell Gila to automatically load in ENV vars that start with GILA
# Note these aren't the same as `bind_env` but are loaded OTF
gila.set_env_prefix('GILA')
gila.automatic_env()

# This would normally be done outside of program
# eg. in docker compose or k8s manifest
os.environ['GILA_HOST'] = 'localhost:9999'

# This is the preferred method for grabbing parameters
# This will resolve the key in the hierarchical fashion
# and gets them OTF
host = gila.get('host')
allow_insecure = gila.get('allow_insecure')

"""Output:
Host: localhost:9999
Insecure allowed: false
"""
print(f'Host: {host}')
print(f'Insecure allowed: {allow_insecure}')

# Let's read in from a file
gila.set_config_file('config.yml')
gila.read_config_file()

# Now let's gather all the configs for easy usage
"""Output:
{'supersecretkey': 11383542091829929728,
 'supersecrettoken': 197398172398172498718024780174,
 'allow_insecure': False, 'host': 'localhost:9999'}
"""
print(gila.all_config())
