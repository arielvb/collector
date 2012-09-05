# -*- coding: utf-8 -*-

import unittest
import mocks
from engine.schema import Schema
from engine import fields


class TestField(unittest.TestCase):

    def setUp(self):
        self.name = 'Fish'

    def test_field_name(self):
        field = fields.Field(self.name)
        self.assertEqual(field.name, self.name)

    def test_field_single_value(self):
        field = fields.Field(self.name)
        self.assertFalse(field.isMultivalue())
        field.setValue('Black')
        self.assertEqual(field.getValue(), 'Black')
        field.setValue('Yellow')
        self.assertEqual(field.getValue(), 'Yellow')
        self.assertRaises(Exception, field.addValue, 'method not allowed')
        self.assertRaises(Exception, field.setValue, ['Black', 'Yellow'])

    def test_field_multivalue(self):
        field = fields.Field(self.name, True)
        self.assertTrue(field.isMultivalue())
        field.addValue('Black')
        self.assertEquals(field.getValue(), ['Black'])
        field.addValue('Yellow')
        self.assertEquals(field.getValue(), ['Black', 'Yellow'])
        field.setValue([])
        self.assertEqual(field.getValue(), [])
        self.assertRaises(Exception, field.setValue, "string aren't allowed, neither basic types")


# class TestField(unittest.TestCase):

#     def test_malformed_field_ref(self):
#         result = Field.validate({'class': 'ref', 'name': 'name', 'ref': 'a.'})
#         self.assertFalse(result)

#     def test_empty_attr_ref_field_ref(self):
#         result = Field.validate({'class': 'ref', 'name': 'name', 'ref': ''})
#         self.assertFalse(result)

# class TestSchemaManager(unittest.TestCase):

#     def test_is_singleton(self):
#         self.assertRaises(Exception, SchemaManager)
#         ins1 = SchemaManager.getInstance()
#         ins2 = SchemaManager.getInstance()
#         self.assertEqual(ins1, ins2)

#     def test_get_non_existing_schema(self):
#         ins = SchemaManager.getInstance()
#         self.assertRaises(Exception, ins.get, 'Fish')

#     def test_get_existing_schema(self):
#         ins = SchemaManager.getInstance()
#         self.assertEqual(ins.get('boardgames').name, 'Boardgames')


class TestSchema(unittest.TestCase):

    def setUp(self):
        self.schema = Schema()
        self.in_values = mocks.collections['boardgames']['schemas']['boardgames']

    def test_loadFromDict_schema(self):
        in_values = self.in_values
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

    def test_is_multivalue(self):
        in_values = self.in_values
        self.schema.loadFromDict(in_values)
        self.assertTrue(self.schema.isMultivalue('designer'))

    def test_is_not_multivalue(self):
        in_values = self.in_values
        self.schema.loadFromDict(in_values)
        self.assertFalse(self.schema.isMultivalue('name'))


if __name__ == '__main__':
    unittest.main()
