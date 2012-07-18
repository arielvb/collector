import os

BASE_PATH = os.path.join(os.path.dirname(__file__), 'data')


schemas = {
    'boardgames': {
        'name': 'Boardgames',
        'fields': {
            'title': {'class': 'text', 'name': 'Title'},
            'desginer': {'class': 'ref', 'name': 'Desginer', 'multiple': True, 'ref': 'people.name'},
            'artist': {'class': 'ref', 'name': 'Artists', 'multiple': True, 'ref': 'people.name'},
            'image': {'class': 'image', 'name': 'Image'}
        }
    },
    'people': {
        'name': 'Authors & Deigners',
        'fields': {
            'name': {'class': 'text', 'name': 'Name'}
        }
    }
}

gameboards = [
    {
        'title': 'The Pillars of the Earth',
        'designer': ['Michael Rieneck', 'Stefan Stadler'],
        'artist': ['Michael Menzel', 'Anke Pohl', 'Thilo Rick'],
        'image': BASE_PATH + '/pilares.jpg'
    },
    {
        'title': 'Coney Island',
        'designer': ['Michael Schant'],
        'artist': ['Dennis Lohausen'],
        'image': BASE_PATH + '/coney-island.jpg'
    }
]

artists = []
for obj in gameboards:
    artists.extend(obj['artist'])


if __name__ == '__main__':
    print gameboards
    print artists
