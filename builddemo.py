#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
""" Pickle demo collection """
from tests.mocks import boardgames, people, collections
import os
import pickle
import json

COLLECTION_NAME = 'demo'
DATA_PATH = os.path.join('data', 'collections', 'demo')
CONFIG_FILE = COLLECTION_NAME + '.json'
# Data (file base name, dictionary)
DATA_FILES = [('people', people), ('boardgames', boardgames)]


def deploy():

    json_it(CONFIG_FILE, collections)
    for item in DATA_FILES:
        pickle_it(item[0] + '.p', item[1])


def json_it(filename, obj):
    data = json.dumps(obj, indent=4)
    f = open(os.path.join(DATA_PATH, filename), 'wb')
    f.write(data)


def pickle_it(filename, obj):
    f = open(os.path.join(DATA_PATH, filename), 'wb')
    pickle.dump(obj, f)
    f.close()

if __name__ == '__main__':
    deploy()
