import unittest

from gila.util.helpers import deep_search, dict_merge
from gila.gila import _allowed_falsy_values


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


class TestDictMerge(unittest.TestCase):

    def test_dict_merge_with_falsy_values(self):
        dict_1, dict_2 = ({}, {})
        for index, falsy_value in enumerate(_allowed_falsy_values):
            dict_1[index] = falsy_value
            dict_2[index] = 'value to overwrite'
        merged_dict = dict_merge(dict_1, dict_2)
        self.assertEqual(merged_dict, dict_1)


if __name__ == '__main__':
    unittest.main()
