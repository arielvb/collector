# -*- coding: utf-8 -*-

import unittest
from engine.collector import Collector


class TestCollector(unittest.TestCase):
    """Collector test case"""

    def test_remap(self):
        """Test for the remap function"""
        data = {'aspect': 'yellow', 'underline': 'false', 'unknow': 'disapear'}
        mapping = {'aspect': 'color', 'underline': 'bold'}
        control = {'color': 'yellow', 'bold': 'false'}
        newdata = Collector.remap(data, mapping)
        self.assertEquals(newdata, control)


if __name__ == '__main__':
    unittest.main()
