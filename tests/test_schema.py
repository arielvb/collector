import unittest
import mocks
from collector.schema import Field, Schema


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

    def test_valid_schema(self):
        self.schema.loadFromDict(mocks.schemas['boardgames'])

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

if __name__ == '__main__':
    unittest.main()
