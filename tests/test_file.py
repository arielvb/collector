# -*- coding: utf-8 -*-

import unittest
from engine.file import File
from engine.fields import *
from engine.schema import Schema


class TestFile(unittest.TestCase):

    def setUp(self):
        schema_def = {
                'name': 'Authors / Designers',
                'fields': {
                    'name': {'class': 'text', 'name': 'Name'}
                },
                'default': 'name',
                'image': ':/author.png',
                'ico': ':ico/author.png'
            }
        self.schema = Schema(schema_def)

    def test_create_whith_wrong_schema(self):
        self.assertRaises(Exception, File, object())

    def test_create_whith_wrong_fields(self):
        file_c = File(Schema(), {'aaa': 'aaaa'})
        self.assertEquals(file_c.fields, {})

    def test_create_empty_schema_empty_fields(self):
        file_c = File(Schema())
        self.assertEquals(file_c.fields, {})

    def test_create_empty_fields(self):
        file_c = File(self.schema)
        self.assertIsInstance(file_c.fields['name'], FieldText)
        self.assertEquals(file_c.fields['name'].value, None)

    def test_create_field_text(self):
        file_c = File(self.schema, {'name': 'Fisherman'})
        self.assertEquals(file_c.fields['name'].value, 'Fisherman')


if __name__ == '__main__':
    unittest.main()
