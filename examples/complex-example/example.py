"""Complex example file.

This example code will show you how we expect the API
to perform with a more complex example of key shadowing,
overrides, aliases, etc. The key point is all original configs
are left untouched. This api provides no way* of overriding system values
for security reasons. This falls on the user to do if so desired.
"""
# Import module and prepend path
import argparse
import os
import gila  # noqa

# Let's read from the CLI
parser = argparse.ArgumentParser()
parser.add_argument("--CC", dest='cc',
                    help="C-compiler flags",
                    type=str, default='')
parser.add_argument("--L", dest='l',
                    help="Linked library flags",
                    type=str, default='')
args = parser.parse_args()

# Efficiently grab all the kwargs
for key, val in args._get_kwargs():
    gila.override(key, val)

# This would normally be done outside of program
# eg. in docker compose or k8s manifest
os.environ['GILA_KEY'] = 'SomeEnvKey'
os.environ['GILA_BOUNDKEY'] = 'SomeBoundEnvKey'

# This will tell Gila to automatically load in ENV vas that start with GILA
# These won't show up in env unless we bind them.
gila.set_env_prefix('GILA')
gila.bind_env('BOUNDKEY')
gila.automatic_env()

# Read in an additional config file
gila.set_config_file('config.yml')
gila.read_in_config()

# create some example configs
aliases = {
    "key2": "aliased_key",
    # "aliased_key": "key2", # This will fail as circular keys are not allowed
}
overrides = {
    "key2": "value1",
    "aliased_key": "value2"
}
default = {
    "key10": "10",
    "key2": "value3",
    "aliased_key": "value4",
    "aliased_dict": {
        "key3": "value6"
    },
    "key_to_alias": {
        "key4": "value64"
    }
}

# Let's load up our configs, the order doesn't matter
for key, alias in aliases.items():
    gila.register_alias(key, alias)
for key, val in overrides.items():
    gila.override(key, val)
for key, val in default.items():
    gila.set_default(key, val)

# What do we expect?
# Notice that alias_key shadows key2 and the subsequent override works
"""Output:
{'key10': '10',
 'aliased_dict': {'key3': 'value6'},
 'noun': 'Hawaii', 'boundkey': 'SomeBoundEnvKey',
 'cc': None, 'l': 'library1,library2,library3',
 'key_to_alias': {'key4': 'value64'}, 'aliased_key': 'value2'}
"""
print(gila.all_config())

# Let's be explicit
"""Output:
aliased_key:  value2
key2:  value2
"""
print('aliased_key: ', gila.get('aliased_key'))
print('key2: ', gila.get('key2'))


# What does the debug show us?
"""Output:
Aliases: {'key2': 'aliased_key'}

Override: {'cc': '', 'l': 'library1,library2,library3',
           'aliased_key': 'value2'}

Env: {'boundkey': 'GILA_BOUNDKEY'}

Config: {'noun': 'Hawaii'}

Defaults: {'key10': '10', 'key2': 'value3',
           'aliased_key': 'value4',
           'aliased_dict': {'key3': 'value6'},
           'key_to_alias': {'key4': 'value64'}}
"""
gila.debug()
