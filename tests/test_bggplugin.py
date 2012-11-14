# -*- coding: utf-8 -*-
# pylint: disable=C0301,C0103, R0904
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
        self.maxDiff = None

    def test_obtain_search_backup(self):
        """Checks that the results from the offline version of the search are
         ok """
        filename = self.data_path + 'geeksearch.php.html'

        provider = FileProvider(filename)

        results = self.plugin.search_filter_html(provider.get('mocked'))
        self.assertItemsEqual(results,
         [
            {'plugin': 'PluginBoardGameGeek',
             'name': u'The Pillars of the Earth', 'year': '2006',
             'id': u'http://boardgamegeek.com/boardgame/24480/' +
             'the-pillars-of-the-earth'},
            {'plugin': 'PluginBoardGameGeek',
             'name': u'The Pillars of the Earth Expansion Set', 'year': '2007',
             'id': u'http://boardgamegeek.com/boardgameexpansion/31753/' +
             'the-pillars-of-the-earth-expansion-set'},
            {'plugin': 'PluginBoardGameGeek',
             'name': u'Die S\xe4ulen der Erde: das Kartenspiel',
             'year': '2010',
             'id': u'http://boardgamegeek.com/boardgame/67593/' +
                'die-saulen-der-erde-das-kartenspiel'}
         ])

    def test_obtain_search_backup_xml(self):
        """Checks that the results from the offline version of the backuped
         xml searchfile are ok.
         The reuslts differ from the source"""
        filename = self.data_path + 'xmlsearch.xml'

        provider = FileProvider(filename)

        results = self.plugin.search_filter(provider.get('mocked'))
        self.assertItemsEqual(results,
         [
            {'plugin': 'PluginBoardGameGeek',
            'id': 'http://boardgamegeek.com/boardgame/24480',
            'name': u'Los Pilares de la Tierra'},
            {'plugin': 'PluginBoardGameGeek',
            'id': 'http://boardgamegeek.com/boardgame/67593',
            'name': u'Los Pilares de la Tierra: El juego de Cartas'},
            {'plugin': 'PluginBoardGameGeek',
            'id': 'http://boardgamegeek.com/boardgame/31753',
            'name': u'Los Pilares de la Tierra: La Expansi\xf3n'}
         ])

    def test_obtain_data_backup_pillars(self):
        """ Checks that all the attributes of the offline version
         are parsed correctly"""
        filename = self.data_path + 'the-pillars-of-the-earth.html'
        provider = FileProvider(filename)
        fields = self.plugin.file_filter(provider.get('mocked'))
        self.assertEquals(fields, {
            'publisher': [u'999 Games', u'Albi',
                          u'Cappelen', u'Competo / MarektoyDevir',
                          u'Filosofia \xc9dition', u'Galakta',
                          u'Kaissa Chess & Games', u'KOSMOS',
                          u'Mayfair Games', u'Stupor Mundi'],
            'designer': [u'Michael Rieneck', u'Stefan Stadler'],
            'bgg_rank': u'141',
            'artist': [u'Michael Menzel', u'Anke Pohl', u'Thilo Rick'],
            'image': 'http://boardgamegeek.com/the-pillars-of-the-earth_files/'
                      'pic212815_md.jpg',
            'title': u'The Pillars of the Earth',
            'min_players': 2,
            'min_age': 12,
            'average': 7.33,
            'mechanic': [u'Worker Placement'],
            'year': 2006,
            'max_players': 4,
            'playing': u'120  minutes',
            'categories': [u'Economic', u'Medieval', u'Novel-based']
        })
        self.assertItemsEqual(fields.keys(), self.plugin.schema.file.keys())

    def test_obtain_data_backup(self):
        """ Checks that all the attributes of the offline version
         are parsed correctly"""
        filename = self.data_path + 'mice-and-mystics.html'
        provider = FileProvider(filename)
        fields = self.plugin.file_filter(provider.get('mocked'))

        self.assertEquals(fields, {
                'publisher': [u'Plaid Hat Games'],
                'designer': [u'Jerry Hawthorne'],
                'bgg_rank': 'N/A',
                'artist': [u'John Ariosa'],
                'title': u'Mice and Mystics',
                'year': 2012,
                'max_players': 4,
                'min_players': 1,
                'min_age': 7,
                'playing': u'60  minutes',
                'categories':
                 [u'Adventure', u'Dice', u'Exploration',
                  u'FantasyFighting', u'Miniatures'],
                'mechanic':
                 [u'Area Movement', u'Co-operative Play', u'Dice Rolling',
                  u'Role PlayingStorytelling', u'Variable Player Powers'],
                 'image': 'http://boardgamegeek.com/mice-and-mystics_files/' +
                          'pic1312072_md.jpg',
                'average': 0.00,
                })
        self.assertItemsEqual(fields.keys(), self.plugin.schema.file.keys())

    def test_min_age_especial_case(self):
        """ Checks that all the attributes of the offline version
         are parsed correctly"""
        filename = self.data_path + 'raze-the-castle.html'
        provider = FileProvider(filename)
        fields = self.plugin.file_filter(provider.get('mocked'))
        self.assertEquals(fields, {
            'publisher': [u'Youngdale Productions'],
            'designer': [u'Jason Youngdale'],
            'artist': [u''],
            'bgg_rank': 'N/A',
            'image': 'http://cf.geekdo-images.com/images/pic432665_md.jpg',
            'title': u'Raze the Castle!',
            'min_players': 2,
            'average': 3.83,
            'mechanic': [u'Dice Rolling', u'Paper-and-Pencil'],
            'year': 2004,
            'max_players': 4,
            'playing': u'120  minutes',
            'categories': [u'Economic', u'Fantasy']
        })
        # self.assertItemsEqual(fields.keys(), self.plugin.schema.file.keys())

    def test_agricola_case(self):
        """This was a test to check why agricola file fails, it wasn't an
        application error, it looks like a bgg network problem. See 
        documentation import errors for more details."""
        filename = self.data_path + 'agricola.html'
        provider = FileProvider(filename)
        fields = self.plugin.file_filter(provider.get('mocked'))
        self.assertEquals(fields, {'publisher': [
            u'999 Games', u'Brain Games',
            u'Compaya.hu - Gamer Caf\xe9 Kft.',
            u'Hobby JapanHobby World', u'HomoLudicus',
            u'Korea Boardgames', u'Lacerta', u'Lookout Games',
            u'MINDOK', u'Smart Ltd', u'Stratelibri',
            u'Swan Panasia Co., Ltd.',
            u'Ystari Games', u'Z-Man Games'],
            'designer': [u'Uwe Rosenberg'],
            'artist': [u'Klemens Franz'], 'bgg_rank': u'2',
            'image': 'http://cf.geekdo-images.com/images/pic259085_md.jpg',
            'title': u'Agricola', 'min_players': 1, 'min_age': 12,
            'average': 8.24, 'mechanic': [u'Worker Placement'],
            'year': 2007, 'max_players': 5, 'playing': u'120  minutes',
            'categories': [u'Economic', u'Farming']}
        )

    def test_int_filter(self):
        """Checks the results of the int filter"""
        self.assertEqual(self.plugin.intfilter('1a'), None)
        self.assertEqual(self.plugin.intfilter('1.1'), None)
        self.assertEqual(self.plugin.intfilter('1'), 1)
        self.assertEqual(self.plugin.intfilter('0'), 0)
        self.assertEqual(self.plugin.intfilter(''), None)
        #Unicode
        self.assertEqual(self.plugin.intfilter(u'100'), 100)







if __name__ == '__main__':
    unittest.main()
