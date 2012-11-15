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

    website = 'http://www.boardgamegeek.com'
    name = 'Boardgamegeek'
    description = "Search and import Boardgames from the BGG website."

    schema = Schema('plugin_bgg', 'boardgames', {
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
                },
                'average': {'name': 'Rating', 'class': 'float'},
                'bgg_rank': {'name': 'BGG Rank'},

            },
            'order': ['title', 'average', 'bgg_rank', 'designer', 'artist',
                      'publisher', 'year', 'min_players', 'max_players',
                      'playing', 'min_age', 'categories', 'mechanic', 'image'],
            'default': 'title',
            'ico': u":/ico/boardgamegeek.png"
        })

    def get_name(self):
        """Returns the name of the plugin"""
        return self.name

    @property
    def icon(self):
        return self.schema.ico

    @classmethod
    def get_author(cls):
        """Returns the author of the plugin"""
        return 'Ariel von Barnekow'

    @classmethod
    def search_uri_xml(cls):
        """Returns the search uri for the boardgamegeek xmlapi"""
        return ("http://boardgamegeek.com/xmlapi/search?search=%s")

    def search_filter_xml(self, html):
        """Returns the search results using the xmlapi of BGG"""
        soup = BeautifulSoup(html)
        base = self.website + "/boardgame/"
        p_id = self.get_id()
        return [{'id': base + i.parent.get("objectid"),
                'name': i.text,
                'plugin': p_id
                } for i in soup.select('name')]

    @classmethod
    def search_uri_html(cls):
        """Returns the search uri pattern"""
        return ("http://boardgamegeek.com/geeksearch.php" +
                "?action=search&objecttype=boardgame&q=%s&B1=Go")

    def search_filter_html(self, html):
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
            year_el = element.find('span')
            # Items without year are articles and not boardgames
            if year_el:
                year = year_el.get_text()
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

    search_uri = search_uri_html
    search_filter = search_filter_html

    def file_filter(self, html):
        """ Parses the html to obtain all the fields defeined in the schema """
        #FIXME # of Players has a dummy encoding,
        #  after beautifulsoup... modify the original string
        html = html.replace('&nbsp;−&nbsp;', ' -     ').replace(
            '&nbsp;&minus;&nbsp;', ' - '
            )
        soup = BeautifulSoup(html, from_encoding="utf-8")
        results = {}
        results['title'] = soup.select('.geekitem_title a span')[0].getText()
        taula = soup.select('.geekitem_infotable')[0]
        rows = taula.findAll('tr')
        results['designer'] = self.row_filter(rows[0])
        results['artist'] = self.row_filter(rows[1])
        results['publisher'] = self.remove_show_more(self.row_filter(rows[2]))
        value = self.intfilter(self.row_filter(rows[3])[0])
        if value is not None:
            results['year'] = value
        num_of_player = self.row_filter(rows[4])[0].split('-')
        value = self.intfilter(num_of_player[0])
        if value is not None:
            results['min_players'] = value
        if len(num_of_player) > 1:
            value = self.intfilter(num_of_player[1])
        if value is not None:
            results['max_players'] = value
        # TODO user_suggested_players field (row 5)
        # TODO unify playing time to minutes
        results['playing'] = ' '.join(self.row_filter(
                                    rows[6])).replace('\t', '')
        min_age = self.intfilter(self.row_filter(rows[7])[0])
        if min_age is not None:
            results['min_age'] = int(min_age)
        # TODO user_suggested_age field (row 8)
        # TODO language_dependence field (row 9)
        # TODO Honors (row 10)
        # TODO subdomain (row 11)
        results['categories'] = (
            self.remove_show_more(self.row_filter(rows[12])))
        results['mechanic'] = self.remove_show_more(self.row_filter(rows[13]))
        # Load image size == medium and not _t
        image = soup.select('link[rel=image_src]')
        if image != []:
            img = soup.select('link[rel=image_src]')[0].get('href').replace(
                '_t', '')
            if not img.startswith('http'):
                img = self.website + '/' + img
            results['image'] = img
        try:
            results['bgg_rank'] = soup.select('.mf.nw.b a')[0].get_text()
        except IndexError:
            results['bgg_rank'] = 'N/A'
        results['average'] = float(soup.select('.b span')[0].get_text())

        return results

    @classmethod
    def intfilter(cls, value):
        """Int filter, returns the int representation of value or None"""
        if isinstance(value, (str, unicode)):
            value = value.strip()
            if value.isdigit():
                return int(value)
            else:
                return None
        elif isinstance(value, int):
            return value
        else:
            return None

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
