# -*- coding: utf-8 -*-
# pylint: disable=C0301,C0103, R0904
# C013 Camecase
"""Test for all the included plugins"""
import unittest
from collector.core.provider import FileProvider
from collector.plugins.boardgamegeek import PluginBoardGameGeek
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

        results = self.plugin.search_filter_xml(provider.get('mocked'))
        self.assertItemsEqual(results,
         [
            {'plugin': 'PluginBoardGameGeek',
            'id': 'http://www.boardgamegeek.com/boardgame/24480',
            'name': u'Los Pilares de la Tierra'},
            {'plugin': 'PluginBoardGameGeek',
            'id': 'http://www.boardgamegeek.com/boardgame/67593',
            'name': u'Los Pilares de la Tierra: El juego de Cartas'},
            {'plugin': 'PluginBoardGameGeek',
            'id': 'http://www.boardgamegeek.com/boardgame/31753',
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
            'image': 'http://www.boardgamegeek.com/the-pillars-of-the-earth_files/'
                      'pic212815.jpg',
            'title': u'The Pillars of the Earth',
            'min_players': 2,
            'min_age': 12,
            'average': 7.33,
            'mechanic': [u'Worker Placement'],
            'year': 2006,
            'max_players': 4,
            'playing': u'120  minutes',
            'categories': [u'Economic', u'Medieval', u'Novel-based'],
            'website': '',
            'description': u"Die S\xe4ulen der Erde / The Pillars of the Earth is based on the bestselling novel by Ken Follett and the 2006 game in the Kosmos line of literature-based games.\nAt the beginning of the 13th century, construction of the greatest \nand most beautiful cathedral in England begins. Players are builders who\n try to contribute the most to this cathedral's construction and, in so \ndoing, score the most victory points. Gameplay roughly consists of \nusing workers to produce raw materials, and then using craftsmen to \nconvert the materials into victory points. Workers may also be used to \nproduce gold, the currency of the game. Players are also given three \nmaster builders each turn, each of which can do a variety of tasks, \nincluding recruiting more workers, buying or selling goods, or just \nobtaining victory points. Getting early choices with a master builder \ncosts gold, as does purchasing better craftsmen. Players must strike a \nbalance between earning gold to fund their purchases and earning victory\n points.\nExpanded by:\n\n The Pillars of the Earth Expansion Set (which include the Expansion Cards in some editions)\n The Pillars of the Earth: Expansion Cards (which are included in the Expansion Set in some editions)\n\nBuy Microbadges\nPillars of the Earth Fan\n http://files.boardgamegeek.com/images/microbadges/pillarsearth.gif \nPillars of the Earth - I pimped my cathedral\n http://files.boardgamegeek.com/images/microbadges/mb_PimpedPillar.gif \n\n Pillars of the Earth fan\n Pillars of the Earth fan\n Pillars of the Earth fan - Exp. Set\n\n",
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
                 'image': 'http://www.boardgamegeek.com/' +
                          'mice-and-mystics_files/pic1312072.jpg',
                'average': 0.00,
                'website': 'http://www.plaidhatgames.com/games/mice-and-mystics',
                'description': u"Game description from the publisher:\nIn Mice and Mystics players take on the \nroles of those still loyal to the king \u2013 but to escape the clutches of \nVanestra, they have been turned into mice! Play as cunning field mice \nwho must race through a castle now twenty times larger than before. The \ncastle would be a dangerous place with Vanestra's minions in control, \nbut now countless other terrors also await heroes who are but the size \nof figs. Play as nimble Prince Colin and fence your way past your foes, \nor try Nez Bellows, the burly smith. Confound your foes as the wizened \nold mouse Maginos, or protect your companions as Tilda, the castle's \nformer healer. Every player will have a vital role in the quest to warn \nthe king, and it will take careful planning to find Vanestra's weakness \nand defeat her.\nMice and Mystics is a cooperative adventure game in which \nthe players work together to save an imperiled kingdom. They will face \ncountless adversaries such as rats, cockroaches, and spiders, and of \ncourse the greatest of all horrors: the castle's housecat, Brodie. Mice and Mystics\n is a boldly innovative game that thrusts players into an ever-changing,\n interactive environment, and features a rich storyline that the players\n help create as they play the game. The Cheese System allows players to \nhorde the crumbs of precious cheese they find on their journey, and use \nit to bolster their mice with grandiose new abilities and overcome \nseemingly insurmountable odds.\nMice and Mystics will provide any group of friends with an \nunforgettable adventure they will be talking about for years to come \u2013 \nassuming they can all squeak by..."
                })
        self.assertItemsEqual(fields.keys(), self.plugin.schema.file.keys())


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
