# -*- coding: utf-8 -*-
"""Test for plugins"""
import unittest
import os
from collector.core.plugin import PluginManager


class TestPluginManager(unittest.TestCase):

    def setUp(self):
        PluginManager._instance = None
        self.manager = PluginManager(
            ['PluginHello'],
            {'PluginHello': type('mock', (str,), {})()})

    def test_disable_not_a_list(self):
        self.assertRaises(TypeError, self.manager.disable, 'PluginHello')

    def test_enable_not_a_list(self):
        self.assertRaises(TypeError, self.manager.enable, 'PluginHello')

    def test_boot_enabled(self):
        self.assertTrue('PluginHello' in self.manager.get_enabled())

    def test_disable_item(self):
        self.assertTrue('PluginHello' in self.manager.get_enabled())
        self.manager.disable(['PluginHello'])
        self.assertFalse('PluginHello' in self.manager.get_enabled())
        self.assertTrue('PluginHello' in self.manager.get_disabled())

    def test_enable_item(self):
        self.manager.disable(['PluginHello'])
        self.assertFalse('PluginHello' in self.manager.get_enabled())
        self.manager.enable(['PluginHello'])
        self.assertTrue('PluginHello' in self.manager.get_enabled())
        self.assertFalse('PluginHello' in self.manager.get_disabled())

    def test_load_enabled_and_run(self):
        path = os.path.join(os.path.dirname(__file__),
                            'data', 'plugins')
        self.manager.look_for_plugins([path])
        execution_result = self.manager.get('PluginHello').results
        self.assertEqual(execution_result, 'Hello world')

    def test_filter(self):
        result = self.manager.filter(str)
        self.assertEquals(result, ['PluginHello'])

if __name__ == '__main__':
    unittest.main()
