"""CLI example file.

This example code will show you how to interface command line flags
with this library. We opted to not include CLI flag interfacing with
the library to give the user the most flexibility for choosing their
own flavour.
"""
# Import module and prepend path
import argparse
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

# Let's print out a single flag
# This is the preferred method for grabbing parameters
# This will resolve the key in the hierarchical fashion
# and gets them OTF
"""Output:
Linked Libraries:  library1,library2
"""
print('Linked Libraries: ', gila.get('l'))

# Grab all configurations
"""Output:
All Flags:  {'l': 'library1,library2', 'cc': 'flag1,flag2'}
"""
print('All Flags: ', gila.all_config())

# Now what does debug show (for testing purposes)
"""Output:
Aliases: {}

Override: {'cc': 'flag1,flag2', 'l': 'library1,library2'}

Env: {}

Config: {}

Defaults: {}

"""
gila.debug()
