# -*- coding: utf-8 -*-
from engine.config import Config
from os import path
config = Config.getInstance()
BASE_PATH = path.join(config.get_appdata_path(), 'collections', 'demo')


boardgames = [
    {
        'id': 1,
        'name': 'The Pillars of the Earth',
        'year': "2007",
        'designer': ['people:1', 'peope:2'],
        'artist': ['people:3', 'people:4', 'people:5'],
        'image': path.join(BASE_PATH, 'pilares.jpg')
    },
    {
        'id': 2,
        'name': 'Coney Island',
        'year': "2010",
        'designer': ['people:6'],
        'artist': ['people:7'],
        'image': path.join(BASE_PATH, 'coney-island.jpg')
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
                    'name': {'class': 'text', 'name': 'Title'},
                    'year': {'class': 'int', 'name': 'Year'},
                    'designer': {'class': 'ref', 'name': 'Designer/s',
                                 'multiple': True,
                                 'params': {'ref': 'people.name'}},
                    'artist': {'class': 'ref', 'name': 'Artist/s',
                               'multiple': True,
                               'params': {'ref': 'people.name'}},
                    'image': {'class': 'image', 'name': 'Image'},
                    'originalidea': {'class': 'text', 'name': 'Original Idea'}
                },
                'default': 'name',
                'order': ['name', 'year', 'designer', 'artist',
                          'image', 'originalidea'],
                'image': ':/boards.png',
                'ico': ':ico/boards.png'
            },
            'people': {
                'name': 'Authors / Designers',
                'fields': {
                    'name': {'class': 'text', 'name': 'Name'}
                },
                'default': 'name',
                'image': ':/author.png',
                'ico': ':ico/author.png'
            },
            'categories': {
                'name': 'Categories',
                'fields': {
                    'name': {'class': 'text', 'name': 'Name'}
                }
            }
        },
        'persistence': {
            'storage': 'pickle',
            # 'parameters': {'boardgames': boardgames, 'people': people}
        }
    }
}

if __name__ == '__main__':
    print boardgames
    print people
