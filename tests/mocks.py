# -*- coding: utf-8 -*-
from engine.config import Config
config = Config.get_instance()
BASE_PATH = 'collector://collections/demo'


boardgames = [
    {
        'id': 1,
        'title': 'The Pillars of the Earth',
        'year': 2007,
        'designer': [1, 2],
        'artist': [3, 4, 5],
        'image': BASE_PATH + '/pilares.jpg'
    },
    {
        'id': 2,
        'title': 'Coney Island',
        'year': 2010,
        'designer': [6],
        'artist': [7],
        'image': BASE_PATH + '/coney-island.jpg'
    }
]

people = [

    {'id': 1, 'name': 'Michael Rieneck'},
    {'id': 2, 'name': 'Stefan Stadler'},
    {'id': 3, 'name': 'Michael Menzel'},
    {'id': 4, 'name': 'Anke Pohl'},
    {'id': 5, 'name': 'Thilo Rick'},
    {'id': 6, 'name': 'Michael Schant'},
    {'id': 7, 'name': 'Dennis Lohausen'}
]

#TODO allow schema option searchable?
collections = {
    'demo': {
        'name': 'Boardgames Demo',
        'protection': 'user',  # Aka, none
        'description': 'Boardgames demo collection',
        'author': 'Ariel',
        'schemas': {
            'boardgames': {
                'name': 'Boardgames',
                'fields': {
                    'title': {'class': 'text', 'name': 'Title'},
                    'year': {'class': 'int', 'name': 'Year'},
                    'designers': {'class': 'ref', 'name': 'Designer/s',
                                 'multiple': True,
                                 'params': {'ref': 'people.name'}},
                    'artists': {'class': 'ref', 'name': 'Artist/s',
                                 'multiple': True,
                                 'params': {'ref': 'people.name'}},
                    'image': {'class': 'image', 'name': 'Image'},
                    'originalidea': {'class': 'text', 'name': 'Original Idea'}
                },
                'default': 'title',
                'order': ['title', 'year', 'designers', 'artists',
                          'image', 'originalidea'],
                'image': ':/boards.png',
                'ico': ':ico/boards.png'
            },
            'people': {
                'name': 'Artists / Designers',
                'fields': {
                    'name': {'class': 'text', 'name': 'Name'}
                },
                'default': 'name',
                'image': ':/author.png',
                'ico': ':ico/author.png'
            },
            # 'categories': {
            #     'name': 'Categories',
            #     'fields': {
            #         'name': {'class': 'text', 'name': 'Name'}
            #     }
            # }
        },
        'persistence': {
            # 'storage': 'pickle',
           'storage': 'sqlalchemy',
            # 'parameters': {'boardgames': boardgames, 'people': people}
        },
        'mappings': {
            'PluginBoardGameGeek': {
                'title': {'field': 'title', 'folder': 'boardgames'},
                'year': {'field': 'year', 'folder': 'boardgames'},
            }
        }
    }
}

if __name__ == '__main__':
    print boardgames
    print people
