# -*- coding: utf-8 -*-

import unittest
import mocks
from engine.schema import Schema


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
#         ins1 = SchemaManager.get_instance()
#         ins2 = SchemaManager.get_instance()
#         self.assertEqual(ins1, ins2)

#     def test_get_non_existing_schema(self):
#         ins = SchemaManager.get_instance()
#         self.assertRaises(Exception, ins.get, 'Fish')

#     def test_get_existing_schema(self):
#         ins = SchemaManager.get_instance()
#         self.assertEqual(ins.get('boardgames').name, 'Boardgames')


class TestSchema(unittest.TestCase):

    def setUp(self):
        self.schema = Schema('demo', 'boardgames')
        self.in_values = mocks.collections['demo']['schemas']['boardgames']

    def test_loadFromDict_schema(self):
        in_values = self.in_values
        self.schema.read_params(in_values)
        self.assertItemsEqual(in_values['fields'], self.schema.fields)
        self.assertItemsEqual(in_values['order'], self.schema.order)
        self.assertEqual(in_values['name'], self.schema.name)

    def test_schema_not_valid_missing_name(self):
        schema = {
            'fields': {}
        }
        self.assertRaises(Exception, self.schema.read_params, schema)

    # def test_schema_missing_ref_field_ref(self):
    #     schema = {'name': 'Wrong ref', 'fields': {
    #             'author': {'class': 'ref', 'name': 'name'}
    #         }
    #     }

    #     self.assertRaises(Exception, self.schema.loadFromDict, schema)

    # def test_is_multivalue(self):
    #     in_values = self.in_values
    #     self.schema.loadFromDict(in_values)
    #     self.assertTrue(self.schema.isMultivalue('designer'))

    # def test_is_not_multivalue(self):
    #     in_values = self.in_values
    #     self.schema.loadFromDict(in_values)
    #     self.assertFalse(self.schema.isMultivalue('name'))

    #     def test_create_whith_wrong_fields(self):
    #     file_c = File(Schema('test', 'boargames',), {'aaa': 'aaaa'})
    #     self.assertEquals(file_c.fields, {})

    # def test_create_empty_schema_empty_fields(self):
    #     file_c = File(Schema('test', 'boargames',))
    #     self.assertEquals(file_c.fields, {})

    # def test_create_empty_fields(self):
    #     file_c = File(self.schema)
    #     self.assertIsInstance(file_c.fields['name'], FieldText)
    #     self.assertEquals(file_c.fields['name'].value, None)

    # def test_create_field_text(self):
    #     file_c = File(self.schema, {'name': 'Fisherman'})
    #     self.assertEquals(file_c.fields['name'].value, 'Fisherman')


if __name__ == '__main__':
    unittest.main()
