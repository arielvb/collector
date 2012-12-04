# -*- coding: utf-8 -*-

import unittest
from engine.controller import Collector


class TestCollector(unittest.TestCase):
    """Collector test case"""

    def test_remap(self):
        """Test for the remap function"""
        data = {'aspect': 'yellow', 'underline': 'false', 'unknow': 'disapear'}
        mapping = {'aspect': 'color', 'underline': 'bold'}
        control = {'color': 'yellow', 'bold': 'false'}
        newdata = Collector.remap(data, mapping)
        self.assertEquals(newdata, control)

    def test_to_single_single(self):
        """Test the multivalue to single conversion, case single value"""
        result = Collector.to_single('a')
        assert result == 'a'

    def test_to_single_from_multivalue(self):
        """Test the multivalue to single conversion, case multivalue value"""
        result = Collector.to_single(['a', 'b', 'c'])
        assert result == 'a'


if __name__ == '__main__':
    unittest.main()
