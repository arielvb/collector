# -*- coding: utf-8 -*-

import unittest
from engine.plugin import PluginManager


class TestPluginManager(unittest.TestCase):

    def setUp(self):
        self.manager = PluginManager(['bgg'])

    def test_disable_not_a_list(self):
        self.assertRaises(TypeError, self.manager.disable, 'bgg')

    def test_enable_not_a_list(self):
        self.assertRaises(TypeError, self.manager.enable, 'bgg')

    def test_boot_enabled(self):
        self.assertTrue('bgg' in self.manager.getEnabled())

    def test_disable_item(self):
        self.manager.disable(['bgg'])
        self.assertFalse('bgg' in self.manager.getEnabled())


if __name__ == '__main__':
    unittest.main()
