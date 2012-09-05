# -*- coding: utf-8 -*-
# pylint: disable=C0301,C0103
# C013 Camecase
"""Test for all the included plugins"""
import unittest
from engine.provider import FileProvider
from plugins.boardgamegeek import PluginBoardGameGeek
from os.path import dirname


class TestBGGPlugin(unittest.TestCase):
    """Tests for the Boargamegeek plugin"""

    def setUp(self):
        """Creates the plugin instance and other common values"""
        self.plugin = PluginBoardGameGeek()
        self.data_path = dirname(__file__) + '/data/bgg/'

    def test_obtain_search_backup(self):
        """Checks that the results from the offline version of the search are
         ok """
        filename = self.data_path + 'geeksearch.php.html'

        provider = FileProvider(filename)

        results = self.plugin.search_filter(provider.get('mocked'))

        self.assertEquals(results, [
            [u'The Pillars of the Earth(2006)',
                u'http://boardgamegeek.com/boardgame/24480/the-pillars-of-the-earth'],
            [u'The Pillars of the Earth Expansion Set(2007)',
                u'http://boardgamegeek.com/boardgameexpansion/31753/the-pillars-of-the-earth-expansion-set'],
            [u'Die S\xe4ulen der Erde: das Kartenspiel(2010)',
                u'http://boardgamegeek.com/boardgame/67593/die-saulen-der-erde-das-kartenspiel']
            ])

    def test_obtain_data_backup(self):
        """ Checks that all the attributes of the offline version are parsed correctly"""
        filename = self.data_path + 'mice-and-mystics.html'
        provider = FileProvider(filename)
        fields = self.plugin.attr_filter(provider.get('mocked'))

        self.assertItemsEqual(fields, {
                'publisher': [u'Plaid Hat Games'],
                'designer': [u'Jerry Hawthorne'],
                'artist': [u'John Ariosa'],
                'title': u'Mice and Mystics',
                'year': 2012,
                'max_players': 4,
                'min_players': 1,
                'min_age': 7,
                'playing': u'60  minutes',
                'categories': [u'Adventure', u'Dice', u'Exploration', u'FantasyFighting', u'Miniatures'],
                'mechanic': [u'Area Movement', u'Co-operative Play', u'Dice Rolling', u'Role PlayingStorytelling', u'Variable Player Powers'],
                })
        self.assertItemsEqual(fields.keys(), self.plugin.schema.fields.keys())


if __name__ == '__main__':
    unittest.main()
