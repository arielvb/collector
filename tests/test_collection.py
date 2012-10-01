# -*- coding: utf-8 -*-

import unittest
from engine.collection import CollectionManager
import os


class TestCollectionManager(unittest.TestCase):

    def setUp(self):
        CollectionManager._instance = None
        self.man = CollectionManager(autodiscover=False)

    def test_is_singleton(self):
        """Checks that obtain the instance again returns the existing one"""
        self.assertEquals(self.man, CollectionManager.get_instance())

    def test_get_app_path(self):
        # ../../data
        collections = self.man.discover_collections(
            os.path.realpath(os.path.join(__file__, "../../data/collections")))
        self.assertEquals(len(collections), 2)

if __name__ == '__main__':
    unittest.main()
