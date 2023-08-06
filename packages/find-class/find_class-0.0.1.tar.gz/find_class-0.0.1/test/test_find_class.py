from unittest import TestCase
from find_class import find_class

class FindClass(TestCase):
    
    def test_class_found(self):
        res = find_class('find_class.find_class.find_class')
        self.assertEqual(find_class, res)

    def test_class_found_via__init__py(self):
        res = find_class('find_class.find_class')
        self.assertEqual(find_class, res)

    def test_class_not_found(self):
        res = find_class('module.dont.exist')
        self.assertFalse(res)