# Gila

Gila is a python3 configuration library based very heavily on the [viper](https://github.com/spf13/viper) config library for Go. It is designed to facilitate making [12 factor](https://12factor.net/) apps as easy as possible using python3.

# Motivation
After having used the Viper config library in Go, I became very used to the ease of use and flexibility that it offered. After looking for a library to use in my python projects I was unable to find one that combined all of the very useful features that Viper supports.

# Features

* Allow default values to be set for each config key
* Automatically find config files on multiple paths
* Load in environment variables automatically that have a specific prefix
* Support most popular config languages: `yaml, toml, json, properties files, hcl, dotenv`
* Singleton pattern for ease of use in most applications

# Installation

Requires python 3.6+

`pip install gila`

# Simple Example
More examples can be found in the examples directory
```python
import gila
from os import environ

# Setting default values for keys
gila.set_default('host', 'localhost:8080')
gila.set_default('allow_insecure', False)

# This will tell Gila to automatically load in ENV vars that start with GILA
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
```

# Supported Config Filetypes
* yaml (`.yaml, .yml`)
* json (`.json`)
* toml (`.toml`)
* hcl (`.hcl`)
* environment variables
  * Values will be cast to strings
  * Keys are cast to lowercase: ENV_VAR -> `gila.get('env_var')`
* properties file (`.properties, .prop, .props`)
  * Values will be cast to strings
* dotenv (`.env`)
  * Values will be cast to strings
  * No nested values supported

# Credits
Steve Francia [spf13](https://github.com/spf13) for creating the Viper library

Authors of [pyyaml](https://github.com/yaml/pyyaml), [pyhcl](https://github.com/virtuald/pyhcl), and [toml](https://github.com/uiri/toml) packages, as Gila would have been much harder to create and maintain without them


# Major differences from Viper

* Case sensitivity - all keys in Gila are case sensitive, this allows for proper json, yaml, and toml support. ENV keys are not case sensitive unless manually bound.
* No support for remote config - while I think that supporting consul and etcd is a very nice feature, I think at this moment in time that it is a feature that belongs in a seperate library.
* No support for command flags - Viper relies pretty heavily on [Cobra](https://github.com/spf13/cobra) companionship for command flags and as of right now Gila has no similar companion library - if you want to make one get in contact, I would be interested in adding this feature.
* Watching for changes in config files - I would very much so like to add this feature, but it is not a feature that I felt was necessary at `v1.0.0`. If you would like this feature you can thumbs up [the issue](https://gitlab.com/dashwav/gila/issues/1), or open a PR with an implementation.
