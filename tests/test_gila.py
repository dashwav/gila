import unittest

from gila.gila import Gila


class TestGila(unittest.TestCase):

    def test_setting_values(self):
        key = "key"
        value = "value"
        gila_instance = Gila()
        gila_instance.set(key, value)
        self.assertEqual(gila_instance.get(key), value)

    def test_setting_default(self):
        key = "key"
        value = "value"
        gila_instance = Gila()
        gila_instance.set_default(key, value)
        self.assertEqual(gila_instance.get(key), value)

    def test_override_precedence_default(self):
        key = "key"
        default_value = "test"
        override_value = "value"
        gila_instance = Gila()
        gila_instance.set_default(key, default_value)
        self.assertEqual(gila_instance.get(key), default_value)
        gila_instance.set(key, override_value)
        self.assertEqual(gila_instance.get(key), override_value)


if __name__ == '__main__':
    unittest.main()
