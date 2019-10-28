import unittest

import gila
from os import environ as os_env
from singleton import singleton_helper


class TestBaseGila(unittest.TestCase):

    def setUp(self):
        gila.reset()

    def test_reset(self):
        key = "key"
        value = "value"
        gila.set(key, value)
        gila.reset()
        self.assertIsNone(gila.get(key))

    def test_setting_values(self):
        key = "key"
        value = "value"
        gila.set(key, value)
        self.assertEqual(gila.get(key), value)

    def test_setting_values_with_alias(self):
        key = "key"
        value = "value"
        gila.set(key, value)
        self.assertEqual(gila.get(key), value)

        alias = "alias_key"
        gila.register_alias(alias, key)
        self.assertEqual(gila.get(alias), value)

    def test_set_env(self):
        key = "GILA_TEST"
        var = "VALUES"
        os_env[key] = var
        gila.bind_env(key)
        self.assertEqual(gila.get(key.lower()), var)

    def test_set_env_with_key(self):
        gila_key = "test"
        key = "GILA_TEST"
        var = "VALUES"
        os_env[key] = var
        gila.bind_env(gila_key, key)
        self.assertEqual(gila.get(gila_key), var)
        self.assertIsNone(gila.get(key))

    def test_set_env_with_prefix(self):
        prefix = "GILA"
        key = "TEST"
        var = "VALUES"
        os_env[f'{prefix}_{key}'] = var
        gila.set_env_prefix(prefix)
        self.assertIsNone(gila.get(key.lower()))
        gila.bind_env(key)
        self.assertEqual(gila.get(key.lower()), var)

    def test_singleton(self):
        key = "test"
        value = "value"
        gila.set(key, value)
        self.assertEqual(gila.get(key), value)
        singleton_helper()
        self.assertEqual(gila.get(key), 'new_value')


class TestOverrides(unittest.TestCase):

    def setUp(self):
        gila.reset()

    def test_override_precedence_env(self):
        key = "gila_key"
        env_value = "test"
        override_value = "value"
        os_env[key.upper()] = env_value
        gila.bind_env(key)
        self.assertEqual(gila.get(key), env_value)
        gila.set(key, override_value)
        self.assertEqual(gila.get(key), override_value)

    def test_env_precendence_config(self):
        key = "filetype"
        env_value = "test"
        gila.set_config_name('yaml_config')
        gila.add_config_path('./tests/configs')
        gila.read_in_config()
        self.assertEqual(gila.get("filetype"), "yaml")
        os_env[key.upper()] = env_value
        gila.bind_env(key)
        self.assertEqual(gila.get(key), env_value)

    def test_config_precendence_default(self):
        key = "filetype"
        default_value = "test"
        gila.set_default(key, default_value)
        self.assertEqual(gila.get(key), default_value)
        gila.set_config_name('yaml_config')
        gila.add_config_path('./tests/configs')
        gila.read_in_config()
        self.assertEqual(gila.get("filetype"), "yaml")


class TestReadConfigs(unittest.TestCase):
    def setUp(self):
        gila.reset()

    def test_auto_env(self):
        prefix = "GILA"
        key = "TEST"
        var = "VALUES"
        os_env[f'{prefix}_{key}'] = var
        gila.automatic_env()
        gila.set_env_prefix(prefix)
        self.assertEqual(gila.get(key), var)

    def test_read_in_yaml(self):
        gila.set_config_name('yaml_config')
        gila.add_config_path('./tests/configs')
        gila.read_in_config()
        self.assertEqual(gila.get("exists"), True)
        self.assertEqual(gila.get("meta.filename"), 'yaml_config')
        self.assertIsInstance(gila.get("contents"), list)

    def test_read_in_prop(self):
        gila.set_config_name('prop_config')
        gila.add_config_path('./tests/configs')
        gila.read_in_config()
        self.assertEqual(gila.get("exists"), 'True')
        self.assertEqual(gila.get("contents.filetype.value_type"), 'string')
        self.assertIsNone(gila.get("contents"))

    def test_read_in_json(self):
        gila.set_config_name('json_config')
        gila.add_config_path('./tests/configs')
        gila.read_in_config()
        self.assertEqual(gila.get("exists"), True)
        self.assertEqual(gila.get("meta.filename"), 'json_config')
        self.assertIsInstance(gila.get("contents"), list)

    def test_read_in_toml(self):
        gila.set_config_name('toml_config')
        gila.add_config_path('./tests/configs')
        gila.read_in_config()
        self.assertEqual(gila.get("exists"), True)
        self.assertEqual(gila.get("meta.filename"), 'toml_config')
        self.assertIsInstance(gila.get("contents"), list)

    def test_read_in_hcl(self):
        gila.set_config_name('hcl_config')
        gila.add_config_path('./tests/configs')
        gila.read_in_config()
        self.assertEqual(gila.get("exists"), True)
        self.assertEqual(gila.get("meta.filename"), 'hcl_config')
        self.assertIsInstance(gila.get("contents"), list)

    def test_read_in_env(self):
        gila.set_config_name('env_config')
        gila.add_config_path('./tests/configs')
        gila.read_in_config()
        self.assertEqual(gila.get("EXISTS"), 'True')


if __name__ == '__main__':
    unittest.main()
