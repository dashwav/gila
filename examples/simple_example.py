import gila
from os import environ

# Setting default values for keys
gila.set_default('host', 'localhost:8080')
gila.set_default('allow_insecure', False)

# This will tell Gila to automatically load in ENV vas that start with GILA
gila.set_env_prefix('GILA')
gila.automatic_env()

# This would normally be done outside of program
# eg. in docker compose or k8s manifest
environ['GILA_HOST'] = 'localhost:9999'

host = gila.get('host')
allow_insecure = gila.get('allow_insecure')

"""
Output:
Host: localhost:9999
Insecure allowed: false
"""
print(f'Host: {host}')
print(f'Insecure allowed: {allow_insecure}')
