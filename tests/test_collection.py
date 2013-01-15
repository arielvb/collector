# -*- coding: utf-8 -*-

import unittest
from collector.core.collection import Collection
from collector.core.persistence_sql import Alchemy
import os


class TestCollection(unittest.TestCase):

    def setUp(self):
        Collection._instance = None
        Alchemy.destroy()
        self.man = Collection(autodiscover=False)

    def test_is_singleton(self):
        """Checks that obtain the instance again returns the existing one"""
        self.assertEquals(self.man, Collection.get_instance())

    def test_discover(self):
        """Tries to discover collections"""
        # TODO move to test_collector
        # ../../data
        collections = self.man.load_collections(
            os.path.realpath(os.path.join(__file__, "../../data/collections")))
        self.assertEquals(len(collections), 2)

    def test_set_properties(self):
        """Test the method set_properties of a collection"""
        name = "A mocked collection"
        author = "Test User"
        description = "Test or not to test"
        self.man._raw = {
            'title': '',
            'author': '',
            'description': '',
        }
        self.man.set_properties({'title': name, 'author': author,
                                 'description': description})
        self.assertEqual(self.man.get_property('title'), name)
        self.man.set_properties({'author': author})
        self.assertEqual(self.man.get_property('author'), author)

        self.man.set_properties({'description': description})
        self.assertEqual(self.man.get_property('description'), description)


if __name__ == '__main__':
    unittest.main()
