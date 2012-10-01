# -*- coding: utf-8 -*-

import unittest
from engine.file import File


class TestFile(unittest.TestCase):

    def setUp(self):
        self.fields = {'fruit': 'apple'}
        alchemy = type('file_alch', (File,), self.fields)
        self.file = alchemy(self.fields)

    def test_crazy_field_name(self):
        fields = {'???á': 'apple'}
        alchemy = type('file_alch', (File,), fields)
        file_ = alchemy(fields)
        self.assertTrue('???á' in file_)

    def test_get_item(self):
        self.assertEquals(self.file['fruit'], 'apple')

    def test_get_using_attr(self):
        self.assertEquals(self.file.fruit, 'apple')

    def test_in(self):
        self.assertTrue('fruit' in self.file)

    def test_set(self):
        self.file['fruit'] = 'orange'
        self.assertEquals(self.file['fruit'], 'orange')
        self.assertEquals(self.file.fruit, 'orange')


if __name__ == '__main__':
    unittest.main()
