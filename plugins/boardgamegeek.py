# -*- coding: utf-8 -*-
# pylint: disable=E1103
# E1103 Instance of BLABLA has no BLABLA member
#  (but some types could not be inferred)

"""Plugin for Boardgamegeek"""

from bs4 import BeautifulSoup
from engine.plugin import PluginCollector
from engine.schema import Schema


class PluginBoardGameGeek(PluginCollector):
    """Boardgamegeek pluginclass"""

    website = 'http://boardgamegeek.com'
    name = 'Boardgamegeek'
    description = "Search and import Boardgames from the BGG website."

    schema = Schema({
            'name': 'Boardgamegeek',
            'fields': {
                'title': {
                    'class': 'text',
                    'name': 'Title',
                    'description': 'Boardgame title'
                    },
                'designer': {
                    'class': 'text',
                    'name': 'Designer/s',
                    'description': 'List of all the designers',
                    'multivalue': True
                    },
                'artist': {
                    'class': 'text',
                    'name': 'Artist/s',
                    'description': 'List of all the artists',
                    'multivalue': True
                    },
                'publisher': {
                    'class': 'text',
                    'name': 'Publisher/s',
                    'description': 'List of all the plublishers',
                    'multivalue': True
                    },
                'year': {
                    'class': 'int',
                    'name': 'Year published',
                    'description': 'Year when the boardgame was published'
                    },
                'min_players': {
                    'class': 'int',
                    'name': 'Min. number of players'
                },
                'max_players': {
                    'class': 'int',
                    'name': 'Max. number of players'
                },
                'playing': {
                    'class': 'text',
                    'name': 'Playing time'
                },
                'min_age': {
                    'class': 'int',
                    'name': 'Mfg suggested ages'
                },
                'categories': {
                    'class': 'text',
                    'name': 'Categories',
                    'multivalue': True
                },
                'mechanic': {
                    'class': 'text',
                    'name': 'Mechanic',
                    'multivalue': True
                },
                'image': {
                    'class': 'image',
                    'name': 'Image',
                }

            },
            'order': ['title', 'designer', 'artist', 'publisher',
                      'year', 'min_players', 'max_players', 'playing',
                      'min_age', 'categories', 'mechanic', 'image'],
            'default': 'title'
        })

    def get_name(self):
        return self.name

    def get_author(self):
        return 'Ariel von Barnekow'

    def search_uri(self):
        return ("http://boardgamegeek.com/geeksearch.php" +
                "?action=search&objecttype=boardgame&q=%s&B1=Go")

    def search_filter(self, html):
        """ Parses the html to obtain all the results of the search """
        selector = ".collection_objectname"
        soup = BeautifulSoup(html)
        results = soup.select(selector)
        output = []
        p_id = self.get_id()
        for element in results:
            name = 'Error'
            name = element.find('a').get_text()
            year = ''
            try:
                year = element.find('span').get_text()
            except:
                pass
            uri = ''
            uri = element.find('a').get('href')

            if not uri.startswith('http'):
                uri = self.website + uri
            output.append({
                'name': name,
                'year': year[1:-1],
                'id': uri,
                'plugin': p_id
                })
        return output

    def file_filter(self, html):
        """ Parses the html to obtain all the fields defeined in the schema """
        #FIXME # of Players has a dummy encoding,
        #  after beautifulsoup... modify the original string
        html = html.replace('&nbsp;−&nbsp;', ' -     ').replace('&nbsp;&minus;&nbsp;',' - ')
        soup = BeautifulSoup(html, 'lxml', from_encoding="utf-8")
        results = {}
        results['title'] = soup.select('.geekitem_title a span')[0].getText()
        taula = soup.select('.geekitem_infotable')[0]
        rows = taula.findAll('tr')
        results['designer'] = self.row_filter(rows[0])
        results['artist'] = self.row_filter(rows[1])
        results['publisher'] = self.remove_show_more(self.row_filter(rows[2]))
        results['year'] = int(self.row_filter(rows[3])[0])
        num_of_player = self.row_filter(rows[4])[0].split('-')
        results['min_players'] = int(num_of_player[0])
        results['max_players'] = int(num_of_player[1])
        # TODO user_suggested_players field (row 5)
        # TODO unify playing time to minutes
        results['playing'] = ' '.join(self.row_filter(
                                    rows[6])).replace('\t', '')
        results['min_age'] = int(self.row_filter(rows[7])[0])
        # TODO user_suggested_age field (row 8)
        # TODO language_dependence field (row 9)
        # TODO Honors (row 10)
        # TODO subdomain (row 11)
        results['categories'] = (
            self.remove_show_more(self.row_filter(rows[12])))
        results['mechanic'] = self.remove_show_more(self.row_filter(rows[13]))
        # Load image size == medium and not _t
        img = soup.select('link[rel=image_src]')[0].get('href').replace('_t', '_md')
        if not img.startswith('http'):
            img = self.website + '/' + img
        results['image'] = img

        return results

    @classmethod
    def row_filter(cls, row):
        """ Filters the content of one row,
        simplifies double line break, and returns a list
        with all the lines"""
        return row.findAll('td')[1].get_text().strip().replace(
                                "\n\n", '').split("\n")

    @classmethod
    def remove_show_more(cls, elements):
        """Removes the last element of the list if it's Show more"""
        if elements[-1] == u'Show More \xbb':
            elements.pop()
        elif elements[-1] == u'Show More &raquo':
            elements.pop()
        return elements
