Welcome to Gila's documentation!
================================
Gila is a python3 configuration library based very heavily on the
Viper_ config library for Go. It is designed to facilitate making
12Factor_ apps as easy as possible using python3.

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

.. _Viper: https://github.com/spf13/viper
.. _12Factor: https://12factor.net/

Requirements
------------

Requires Python 3.6+

Features
--------

* Easily load in config values for use in your 12factor application
* Allow default values to be set for each config key
* Automatically find config files on multiple paths
* Load in environment variables automatically that have a specific prefix
* Support most popular config languages: `yaml, toml, json, properties files, hcl, dotenv`
* Singleton pattern for ease of use in most applications

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
