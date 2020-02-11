Gila
================================

.. image:: https://img.shields.io/gitlab/pipeline/dashwav/gila/develop
    :target: https://gitlab.com/dashwav/gila/pipelines
    
.. image:: https://img.shields.io/pypi/v/gila
    :target: https://pypi.org/project/gila/ 

.. image:: https://img.shields.io/pypi/pyversions/gila
    :target: https://pypi.org/project/gila/

.. image:: https://api.codacy.com/project/badge/Grade/a911b2a08953491aab19a3171e556aa9
    :target: https://app.codacy.com/manual/dashwav/gila/dashboard
 
Gila is a python3 configuration library based very heavily on the
Viper_ config library for Go. It is designed to facilitate making
12Factor_ apps as easy as possible using python3.

Example Usage:

::

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
    
    # This is the preferred method of grabbing
    # the configurations. Other methods exist (all_config, debug)
    # but this method is the most performant for single
    # value calls.
    host = gila.get('host')
    allow_insecure = gila.get('allow_insecure')
    
    """
    Output:
    Host: localhost:9999
    Insecure allowed: false
    """
    print(f'Host: {host}')
    print(f'Insecure allowed: {allow_insecure}')


.. _Viper: https://github.com/spf13/viper
.. _12Factor: https://12factor.net/

Features
--------

* Easily load in config values for use in your 12factor application
* Allow default values to be set for each config key
* Automatically find config files on multiple paths
* Load in environment variables automatically that have a specific prefix
* Support most popular config languages: `yaml, toml, json, properties files, hcl, dotenv`
* Singleton pattern for ease of use in most applications

You can either use the Gila library as a singleton pattern, by using

::

    import gila

    gila.get("key")

or you can create an instance to use in your application like this

::

    import gila

    gila_instance = Gila()
    gila_instance.get("key")

All functions of the gila class are available in the singleton instance
with the addition of ``gila.reset()``, which will reset the singleton
instance back to empty.

Contents
-----------------------

.. toctree::
   :maxdepth: 1

   gila
   install


License
---------------
Gila is released under the MPL2.0 License. See
`LICENSE file <https://gitlab.com/dashwav/gila/blob/docs-WIP/LICENSE>`_
for details.
