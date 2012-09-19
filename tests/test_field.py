# -*- coding: utf-8 -*-

import unittest
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
        self.assertRaises(Exception, field.setValue,
                          "string aren't allowed, neither basic types")


class TestFieldInt(unittest.TestCase):

    def test_setValue_with_correct_str(self):
        field = fields.FieldInt('A name', False)
        field.setValue('1')
        self.assertEquals(field.getValue(), 1)
        field.setValue('89999')
        self.assertEquals(field.getValue(), 89999)
        field.setValue('00002')
        self.assertEquals(field.getValue(), 2)

    def test_addValue_as_str(self):
        field = fields.FieldInt('A name', True)
        field.addValue(['1'])
        self.assertEquals(field.getValue(), [1])

    def test_setValue_with_int(self):
        field = fields.FieldInt('A name', False)
        field.setValue(1)
        self.assertEquals(field.getValue(), 1)

    def test_setValue_with_non_valid_values(self):
        field = fields.FieldInt('A name', False)
        self.assertRaises(ValueError, field.setValue, "1.0")
        self.assertRaises(ValueError, field.setValue, "asdfasdf")


class TestFieldLoader(unittest.TestCase):

    def setUp(self):
        fields._fieldManagerInstance = None
        self.man = fields.FieldManager()

    def test_non_existing_field_type(self):
        nonexisiting_id = 'asasdfas'
        fake_schema = {'class': nonexisiting_id}
        self.assertRaises(fields.FieldClassNotFound, self.man.get,
                          fake_schema)

    def test_load_text_field(self):
        fake_schema = {
            "class": 'text',
            "name": 'Title',
            "multivalue": False
        }
        result = self.man.get(fake_schema)
        self.assertTrue(isinstance(result, fields.FieldText))

    def test_load_int_field(self):
        fake_schema = {
            "class": 'int',
            "name": 'Year',
            "multivalue": False
        }
        result = self.man.get(fake_schema)
        self.assertTrue(isinstance(result, fields.FieldInt))


if __name__ == '__main__':
    unittest.main()
