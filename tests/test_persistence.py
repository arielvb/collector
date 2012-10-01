# -*- coding: utf-8 -*-
import unittest
from engine.persistence import PersistenceDict
import sqlalchemy
from mocks import boardgames
from engine.persistence_sql import Alchemy, PersistenceAlchemy


class TestPersistence(unittest.TestCase):

    def setUp(self):
        schema = type('Schema', (object,),
                 dict(collection='demo', id='boardgames'))

        self.manager = PersistenceDict(schema, path=None,
                params={'data': boardgames})

    def tearDown(self):
        pass

    def test_get_by_id(self):
        self.assertEquals(self.manager.get(1)['id'], 1)
        self.assertEquals(self.manager.get(2)['id'], 2)
        # Using strings
        self.assertEquals(self.manager.get("1")['id'], 1)
        self.assertEquals(self.manager.get("2")['id'], 2)

    def test_search(self):
        items = self.manager.search('The Pillars of the Earth')
        self.assertEqual(len(items), 1)
        # Search multple items (e appears in the 2 demo objects)
        items = self.manager.search('e')
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]['title'], 'The Pillars of the Earth')
        self.assertEqual(items[1]['title'], 'Coney Island')


class TestAlchemy(unittest.TestCase):
    """TestAlchemy, testcase for the Alchemy class of persistence_sql"""

    def setUp(self):
        Alchemy.destroy()
        self.alchemy = Alchemy()

    def tearDown(self):
        Alchemy.destroy()

    def test_alchemy_singleton(self):
        self.assertEquals(Alchemy.get_instance(), self.alchemy)

    def test_exception_when_called_constructor(self):
        self.assertRaises(Exception, Alchemy)

    def test_get_engine(self):
        engine = self.alchemy.get_engine(":memory:")
        engine2 = self.alchemy.get_engine(":memory:")
        self.assertTrue(isinstance(engine, sqlalchemy.engine.base.Engine))
        self.assertEqual(engine, engine2)

    def test_get_session(self):
        self.alchemy.get_engine(":memory:")
        self.alchemy.get_session(":memory:")
        #TODO check results of get_session

    def test_exception_get_session_non_existing_engine(self):
        self.assertRaises(Exception, self.alchemy.get_session, ":memory:")


class TestPersistenceAlchemy(unittest.TestCase):

    def setUp(self):
        field = type("Field", (object, ), {'name': '', '_class': '',
                           'get_id': lambda s: 'field1'})
        field1 = field()
        field1.name = 'Name'
        field1._class = 'ref'

        self.schema = type("Schema", (object,), {'collection': 'test',
                           'id': 'browser',
                           'file': {'field1': field1}})

    def test_add_using_memory(self):
        """Using :memory: no file is create in the filesystem"""
        pers = PersistenceAlchemy(self.schema(), ':memory:')
        nuevo = pers._class({'name': 'No, gracias'})
        pers._session.add(nuevo)
        pers._session.commit()
        self.assertEqual(nuevo.id, 1)
        result = pers._session.query(pers._class).first()
        # self.assertEqual(nuevo, result)

    def test_add_using_save(self):
        pers = PersistenceAlchemy(self.schema(), ':memory:')

        result = pers.save({'name': 'John'})
        self.assertEqual(result.name, 'John')
        result = pers._session.query(pers._class).first()



if __name__ == '__main__':
    unittest.main()
