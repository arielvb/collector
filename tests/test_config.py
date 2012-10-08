# -*- coding: utf-8 -*-

import unittest
from engine import config
import sys
import os


class TestConfig(unittest.TestCase):

    def setUp(self):
        config.rebuild_constants()
        config.Config._instance = None

    def test_rebuild_constants(self):
        check = config.ISWINDOWS
        config.ISWINDOWS = not check
        config.rebuild_constants()
        self.assertEquals(config.ISWINDOWS, check)

    def test_resources_non_frozen_mac(self):
        conf = config.Config(platform=config.Config.OSX)
        path = conf.get_resources_path()
        self.assertEquals(path, os.path.abspath(''))

    def test_resources_frozen_mac(self):
        setattr(sys, 'frozen', 'macosx_app')
        conf = config.Config(platform=config.Config.OSX)
        path = conf.get_resources_path()
        delattr(sys, 'frozen')
        ok = os.path.dirname(sys.executable).replace('MacOS',
                 'Resources')
        self.assertEquals(path, ok)

    def test_resources_non_frozen_win(self):
        sys.platform = "win32"
        config.rebuild_constants()
        conf = config.Config()
        path = conf.get_resources_path()
        self.assertEquals(path, os.path.abspath(''))

    def test_resources_frozen_win(self):
        setattr(sys, 'frozen', 'windows')
        conf = config.Config(platform=config.Config.WINDOWS)
        path = conf.get_resources_path()
        delattr(sys, 'frozen')
        ok = os.path.dirname(sys.executable)
        self.assertEquals(path, ok)

    def test_config_directory_win(self):
        conf = config.Config(platform=config.Config.WINDOWS)
        self.assertEquals(
            conf.get_data_path(),
            os.path.join(os.path.expanduser('~'), 'Collector'))

    #TODO linux config!


if __name__ == '__main__':
    unittest.main()
