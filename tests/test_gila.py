import unittest

import gila.gila as gila


class TestGila(unittest.TestCase):

    def test_setting_values(self):
        key = "key"
        value = "value"
        gila.set(key, value)
        self.assertEqual(gila.get(key), value)

    def test_setting_default(self):
        key = "key"
        value = "value"
        gila.set_default(key, value)
        self.assertEqual(gila.get(key), value)

    def test_override_precedence_default(self):
        key = "key"
        default_value = "test"
        override_value = "value"
        gila.set_default(key, default_value)
        self.assertEqual(gila.get(key), default_value)
        gila.set(key, override_value)
        self.assertEqual(gila.get(key), override_value)


if __name__ == '__main__':
    unittest.main()
