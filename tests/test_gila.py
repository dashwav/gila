import unittest

from gila.gila import Gila


class TestGila(unittest.TestCase):

    def test_setting_values(self):
        key = "key"
        value = "value"
        gila_instance = Gila()
        gila_instance.set(key, value)
        self.assertEqual(gila_instance.get(key), value)


if __name__ == '__main__':
    unittest.main()
