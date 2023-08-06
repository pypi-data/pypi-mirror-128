from unittest import TestCase
from map_as_object import as_object

class TestMapAsObject(TestCase):

    def test_wraps_map(self):
        m = as_object({'a': 1})
        self.assertEqual(1, m.a)

    def test_entry_not_in_map(self):
        m = as_object({'a': 1})
        with self.assertRaises(AttributeError):
            m.b
