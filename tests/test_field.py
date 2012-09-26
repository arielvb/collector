# -*- coding: utf-8 -*-

import unittest
from engine import fields


class TestField(unittest.TestCase):

    def setUp(self):
        self.name = 'Fish'

    def test_field_name(self):
        field = fields.FieldText(self.name)
        self.assertEqual(field.name, self.name)

    def test_field_single_value(self):
        field = fields.FieldText(self.name)
        self.assertFalse(field.is_multivalue())
        field.set_value('Black')
        self.assertEqual(field.get_value(), 'Black')
        field.set_value('Yellow')
        self.assertEqual(field.get_value(), 'Yellow')
        self.assertRaises(TypeError, field.add_value, 'method not allowed')
        self.assertRaises(ValueError, field.set_value, ['Black', 'Yellow'])

    def test_field_multivalue(self):
        field = fields.FieldText(self.name, True)
        self.assertTrue(field.is_multivalue())
        field.add_value('Black')
        self.assertEquals(field.get_value(), ['Black'])
        field.add_value('Yellow')
        self.assertEquals(field.get_value(), ['Black', 'Yellow'])
        field.set_value([])
        self.assertEqual(field.get_value(), [])
        self.assertRaises(ValueError, field.set_value,
                          "string aren't allowed, neither basic types")


class TestFieldInt(unittest.TestCase):

    def test_set_value_with_correct_str(self):
        field = fields.FieldInt('A name', False)
        field.set_value('1')
        self.assertEquals(field.get_value(), 1)
        field.set_value('89999')
        self.assertEquals(field.get_value(), 89999)
        field.set_value('00002')
        self.assertEquals(field.get_value(), 2)

    def test_add_value_as_str(self):
        field = fields.FieldInt('A name', True)
        field.add_value(['1'])
        self.assertEquals(field.get_value(), [1])

    def test_set_value_with_int(self):
        field = fields.FieldInt('A name', False)
        field.set_value(1)
        self.assertEquals(field.get_value(), 1)

    def test_set_value_with_non_valid_values(self):
        field = fields.FieldInt('A name', False)
        self.assertRaises(ValueError, field.set_value, "1.0")
        self.assertRaises(ValueError, field.set_value, "asdfasdf")

from engine.config import Config
from os.path import join


class TestFieldImage(unittest.TestCase):

    def test_collector_scheme(self):
        field = fields.FieldImage('image')
        field.set_value('collector://collections/demo/demo.png')
        self.assertEqual(join(Config.get_instance().get_data_path(),
                              'collections', 'demo', 'demo.png'),
                              field.get_value())


class TestFieldRef(unittest.TestCase):

    def test_missing_param_ref(self):
        self.assertRaises(Exception, fields.FieldRef,
                          'ooops')

    def test_wrong_format_of_ref(self):
        self.assertRaises(Exception, fields.FieldRef,
                          'ooops', params={'ref': 'a'})


class TestFieldManager(unittest.TestCase):

    def setUp(self):
        fields.FieldManager._instance = None
        self.man = fields.FieldManager()

    def test_execpection_without_name(self):
        fake_schema = {'class': 'text'}
        self.assertRaises(ValueError, self.man.get,
                          fake_schema)

    def test_non_existing_field_type(self):
        nonexisiting_id = 'asasdfas'
        fake_schema = {'class': nonexisiting_id, 'name': 'Fish'}
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
