import unittest

from gila.helpers import deep_search


class TestDeepSearch(unittest.TestCase):

    def test_non_dict_haystack(self):
        non_dict = 'test string'
        with self.assertRaises(TypeError):
            deep_search(non_dict, ['test'])

    def test_non_list_path(self):
        non_dict = {}
        with self.assertRaises(TypeError):
            deep_search(non_dict, 'test')

    def test_deep_search_overwrite_l3(self):
        haystack = {
            'foo': {
                'bar': 'test'
            },
            'test': True
        }
        path = ['foo', 'bar', 'baz']
        deepest_dict = deep_search(haystack, path)

        # Value returned is dict
        self.assertIsInstance(deepest_dict, dict)
        # Original map is not edited
        self.assertIsNotNone(haystack['test'])

        # Returned dict is reference to haystack
        deepest_dict['test'] = True
        self.assertIsNotNone(haystack['foo']['bar']['baz']['test'])

    def test_deep_search_overwrite_none(self):
        haystack = {
            'foo': {
                'bar': {
                    'baz': {
                        'test': True
                    }
                }
            }
        }
        path = ['foo', 'bar', 'baz']
        deepest_dict = deep_search(haystack, path)

        # Value returned is dict
        self.assertIsInstance(deepest_dict, dict)

        # Original map is not edited
        self.assertIsNotNone(haystack['foo']['bar']['baz']['test'])

        # Returned dict is reference to haystack
        deepest_dict['test'] = False
        self.assertFalse(haystack['foo']['bar']['baz']['test'])

    def test_deep_search_all_create(self):
        haystack = {}
        path = ['foo', 'bar', 'baz']
        deepest_dict = deep_search(haystack, path)

        # Value returned is dict
        self.assertIsInstance(deepest_dict, dict)

        # Returned dict is reference to haystack
        deepest_dict['test'] = True
        self.assertIsNotNone(haystack['foo']['bar']['baz']['test'])


if __name__ == '__main__':
    unittest.main()
