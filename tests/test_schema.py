# -*- coding: utf-8 -*-

import unittest
import mocks
from engine.schema import Schema
from engine.fields import Field


class TestField(unittest.TestCase):

    def test_malformed_field_ref(self):
        result = Field.validate({'class': 'ref', 'name': 'name', 'ref': 'a.'})
        self.assertFalse(result)

    def test_empty_attr_ref_field_ref(self):
        result = Field.validate({'class': 'ref', 'name': 'name', 'ref': ''})
        self.assertFalse(result)


class TestSchema(unittest.TestCase):

    def setUp(self):
        self.schema = Schema()

    def test_loadFromDict_schema(self):
        in_values = mocks.schemas['boardgames']
        self.schema.loadFromDict(in_values)
        self.assertItemsEqual(in_values['fields'], self.schema.fields)
        self.assertItemsEqual(in_values['order'], self.schema.order)
        self.assertEqual(in_values['name'], self.schema.name)

    def test_schema_not_valid_missing_name(self):
        schema = {
            'fields': {}
        }
        self.assertRaises(Exception, self.schema.loadFromDict, schema)

    def test_schema_missing_ref_field_ref(self):
        schema = {'name': 'Wrong ref', 'fields': {
                'author': {'class': 'ref', 'name': 'name'}
            }
        }

        self.assertRaises(Exception, self.schema.loadFromDict, schema)

    def test_is_multiple(self):
        in_values = mocks.schemas['boardgames']
        self.schema.loadFromDict(in_values)
        self.assertTrue(self.schema.isMultiple('designer'))

    def test_is_not_multiple(self):
        in_values = mocks.schemas['boardgames']
        self.schema.loadFromDict(in_values)
        self.assertFalse(self.schema.isMultiple('name'))

if __name__ == '__main__':
    unittest.main()
