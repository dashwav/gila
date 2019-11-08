"""Alias example file.

This example code will show you how aliases work with gila.
This also shows off more explicitely how the hierarchical system works.
"""
# Import module and prepend path
import gila  # noqa

# Reading in our example config file.
gila.set_config_file('config.yml')
gila.read_in_config()

# This is the preferred method for grabbing parameters
# This will resolve the key in the hierarchical fashion
# and gets them OTF
"""Output:
supersecrettoken:  197398172398172498718024780174
"""
print('supersecrettoken: ', gila.get('supersecrettoken'))

# Now let's alias one of the keys.
# Notice both work, they actually link to the same data.
gila.register_alias('notasecret', 'supersecrettoken')
"""Output:
supersecrettoken:  197398172398172498718024780174
notasecret:  197398172398172498718024780174
"""
print('supersecrettoken: ', gila.get('supersecrettoken'))
print('notasecret: ', gila.get('notasecret'))

# Now let's try changing the keys. One at a time
gila.override('supersecrettoken', 'is this changed?')
"""Output:
Changing with supersecrettoken only
supersecrettoken:  is this changed?
notasecret:  is this changed?
"""
print('Changing with supersecrettoken only')
print('supersecrettoken: ', gila.get('supersecrettoken'))
print('notasecret: ', gila.get('notasecret'))

gila.override('notasecret', 'is this changed...again?')
"""Output:
Changing with notasecret only
supersecrettoken:  is this changed...again?
notasecret:  is this changed...again?
"""
print('Changing with notasecret only')
print('supersecrettoken: ', gila.get('supersecrettoken'))
print('notasecret: ', gila.get('notasecret'))

# Now check what is happening under the hood
# Notice, the configs themselves are untouched.
"""Output:
Aliases: {'notasecret': 'supersecrettoken'}

Override: {'supersecrettoken': 'is this changed...again?'}

Env: {}

Config: {'supersecrettoken': 197398172398172498718024780174,
         'supersecretkey': 11383542091829929728}

Defaults: {}
"""
gila.debug()

# And finally tear it down.
gila.deregister_alias('supersecrettoken')
"""Output:
supersecrettoken:  is this changed?
notasecret:  is this changed?
"""
print('supersecrettoken: ', gila.get('supersecrettoken'))
print('notasecret: ', gila.get('notasecret'))

# what does our debug show?
"""Output:
Aliases: {'notasecret': 'supersecrettoken'}

Override: {'supersecrettoken': 'is this changed?',
           'notasecret': 'is this changed...again?'}

Env: {}

Config: {'supersecrettoken': 197398172398172498718024780174,
         'supersecretkey': 11383542091829929728}

Defaults: {}
"""
gila.debug()
