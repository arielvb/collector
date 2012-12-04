# -*- coding: utf-8 -*-
import unittest
from collector.core.persistence import PersistenceDict
from collector.core.fields import *
from collector.core.schema import Schema
import sqlalchemy
from mocks import boardgames
from collector.core.persistence_sql import Alchemy, PersistenceAlchemy


class TestPersistence(unittest.TestCase):
    """Persistence class tests"""

    def setUp(self):
        """Test setup"""
        schema = type('Schema', (object,),
                 dict(collection='demo', id='boardgames'))
        Config.get_instance().set_home('/tmp/', True)
        self.manager = PersistenceDict(schema, path="/tmp/collections/demo/",
                params={'data': boardgames})

    def test_get_by_id(self):
        """Cheks the get_id method"""
        self.assertEquals(self.manager.get(1)['id'], 1)
        self.assertEquals(self.manager.get(2)['id'], 2)
        # Using strings
        self.assertEquals(self.manager.get("1")['id'], 1)
        self.assertEquals(self.manager.get("2")['id'], 2)

    def test_search(self):
        """Test the search method"""
        items = self.manager.search('The Pillars of the Earth')
        self.assertEqual(len(items), 1)
        # Search multple items (e appears in the 2 demo objects)
        items = self.manager.search('e')
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]['title'], 'The Pillars of the Earth')
        self.assertEqual(items[1]['title'], 'Coney Island')

    def test_addfile(self):
        """Test for the addfile method"""
        name = self.manager.addfile(__file__, 'http')

        self.assertEquals(name, __file__)
        name = self.manager.addfile(__file__, 'always')
        image = FieldImage('Fish')
        image.set_value(name)
        name = image.get_value()
        self.assertEquals(open(name, "r").read(), open(__file__, "r").read())


class TestAlchemy(unittest.TestCase):
    """TestAlchemy, testcase for the Alchemy class of persistence_sql"""

    def setUp(self):
        """Test setup"""
        Alchemy.destroy()
        # To enable the echo option of SQLAlchemy just change this to True
        Alchemy.echo = False
        self.alchemy = Alchemy()

    def tearDown(self):
        """Test teardown"""
        Alchemy.destroy()

    def test_alchemy_singleton(self):
        """Check alchemy is a manager"""
        self.assertEquals(Alchemy.get_instance(), self.alchemy)

    def test_exception_constructor(self):
        """Check that only one isnstace of alchemy can be created"""
        self.assertRaises(Exception, Alchemy)

    def test_get_engine(self):
        """Creation and retrival of an engine"""
        engine = self.alchemy.get_engine(":memory:")
        engine2 = self.alchemy.get_engine(":memory:")
        self.assertTrue(isinstance(engine, sqlalchemy.engine.base.Engine))
        self.assertEqual(engine, engine2)

    def test_get_session(self):
        """Creation and retrival of a session"""
        self.alchemy.get_engine(":memory:")
        self.alchemy.get_session(":memory:")
        #TODO check results of get_session

    def test_exception_get_session(self):
        """Exception if we try to retrieve session for a non exising engine"""
        self.assertRaises(Exception, self.alchemy.get_session, ":memory:")


class TestPersistenceAlchemy(unittest.TestCase):

    def setUp(self):
        field1 = FieldText('Name')

        self.schema = Schema('test', 'browser')
        self.schema.add_field(field1)
        self.pers = PersistenceAlchemy(self.schema, ':memory:')

    def test_add_using_memory(self):
        """Using :memory: no file is create in the filesystem"""
        pers = self.pers
        pers.all_created()
        nuevo = pers.class_({'name': 'No, gracias'})
        pers._session.add(nuevo)
        pers._session.commit()
        self.assertEqual(nuevo.id, 1)
        result = pers._session.query(pers.class_).first()
        self.assertEqual(nuevo, result)

    def test_add_using_save(self):
        pers = self.pers
        pers.all_created()
        obj = pers.save({'name': 'John'})
        self.assertEqual(obj.name, 'John')
        self.assertEqual(obj.id, 1)
        result = pers._session.query(pers.class_).first()
        self.assertEquals(obj, result)

    def test_delete(self):
        self.pers.all_created()
        obj = self.pers.save({'name': 'John'})
        self.pers.delete(obj.id)
        self.assertEqual(self.pers.get(obj.id), None)

    def test_search(self):
        pers = self.pers
        pers.all_created()
        pers.save({'name': 'John'})
        pers.save({'name': 'Jonas'})
        pers.save({'name': 'Ralph'})
        # lower
        results = pers.search('jo')
        names = [i.name for i in results]
        self.assertEquals(names, [u'John', u'Jonas'])
        # upper
        results = pers.search('JO')
        names = [i.name for i in results]
        self.assertEquals(names, [u'John', u'Jonas'])
        # exact
        results = pers.search('Jo')
        names = [i.name for i in results]
        self.assertEquals(names, [u'John', u'Jonas'])

    def test_text_multivalue(self):

        field1 = FieldText('Name', True)

        schema = Schema('test', 'boardgames')
        schema.add_field(field1)
        pers = PersistenceAlchemy(schema, ':memory:')
        pers.all_created()

        obj = pers.save({'name': ['Rufus', 'Karl']})
        self.assertEquals(obj.name, ['Rufus', 'Karl'])

        # Also you can append a name after construct
        obj.name.append('Julius')
        self.assertEquals(obj.name, ['Rufus', 'Karl', 'Julius'])
        # Update the existing entry
        obj2 = pers.save({'name': 'Homer', 'id': obj.id})
        self.assertEquals(obj.name, ['Homer'])
        # The first object and the last are the same
        self.assertEqual(obj, obj2)

    def test_int_multivalue(self):

        field1 = FieldInt('Count', True)

        schema = Schema('test', 'boardgames')
        schema.add_field(field1)
        pers = PersistenceAlchemy(schema, ':memory:')
        pers.all_created()
        obj = pers.save({'count': [1, 2]})
        self.assertEquals(obj['count'], [1, 2])
        self.assertEquals(obj.count, [1, 2])

    def test_filter_equal(self):
        """Test the Equals filter"""
        self.pers.all_created()
        self.pers.save({'name': 'John'})
        self.pers.save({'name': 'Robert'})

        params = [{'equals': ['name', 'John']}]
        results = self.pers.filter(params)
        self.assertEquals([i.name for i in results], ['John'])

    def test_filter_like(self):
        """Test the like filter, a text is contained inside other"""
        self.pers.all_created()
        self.pers.save({'name': 'John'})
        self.pers.save({'name': 'Robert'})
        params = [{'like': ['name', 'o']}]

        results = self.pers.filter(params)
        self.assertEquals([i.name for i in results], ['John', 'Robert'])

    def test_filter_join(self):
        self.pers.all_created()
        self.pers.save({'name': 'John Deere'})
        self.pers.save({'name': 'Johny Deep'})
        params = [{'like': ['name', 'o']}, {'like': ['name', 'ep']}]
        results = self.pers.filter(params)
        self.assertEquals([i.name for i in results], ['Johny Deep'])

    def test_get_all(self):
        pers = self.pers
        pers.all_created()
        pers.save({'name': 'Robert'})
        pers.save({'name': 'Carl'})
        pers.save({'name': 'Aron'})
        one = pers.get_all(1, 0, None)
        self.assertEqual(len(one), 2)
        self.assertEqual(one[0].name, 'Carl')
        one = pers.get_all(2, 1, None)
        self.assertEqual(len(one), 1)
        self.assertEqual(one[0].name, 'Aron')
        results = pers.get_all(0, 0, u'name')
        self.assertEquals(['Aron', 'Carl', 'Robert'],
                          [i.name for i in results])

    def tearDown(self):
        Alchemy.destroy()


class TestPersistenceAlchemyReferences(unittest.TestCase):

    def setUp(self):
        field1 = FieldText('Name')

        schema = Schema('test', 'browser')
        schema.add_field(field1)
        self.pers = PersistenceAlchemy(schema, ':memory:')
        field2 = FieldRef('Designer', params={'ref': 'browser.name'})

        field1 = FieldText('Name')

        field3 = FieldRef('Artist', params={'ref': 'browser.name'})

        schema = Schema('test', 'designers')

        schema.add_field(field1)
        schema.add_field(field2)
        schema.add_field(field3)

        self.pers2 = PersistenceAlchemy(schema, ':memory:')
        self.pers2.all_created()

        self.pers.save({'name': 'John'})
        self.pers.save({'name': 'Julius'})

    def test_ref_save(self):
        pers2 = self.pers2
        ref = pers2.save({'name': 'Game1', 'designer': 1, 'artist': 2})
        self.assertEqual(ref.name, 'Game1')
        self.assertEqual(ref.designer, 1)
        self.assertEqual(ref.designer_relation.name, 'John')
        db = pers2.engine.execute("SELECT * FROM designers").fetchall()
        self.assertEquals(db, [(1, 1, u'Game1', 2)])

    def test_ref_update_existing(self):
        pers2 = self.pers2
        ref = pers2.save({'name': 'Game1', 'designer': 1, 'artist': 2})
        new_value = {'id': ref.id, 'name': 'Pilares',
                     'designer': 2, 'artist': 1}
        pers2.save(new_value)
        db = pers2.engine.execute("SELECT * FROM designers").fetchall()
        self.assertEquals(db, [(1, 2, u'Pilares', 1)])

    def test_ref_load_references(self):
        pers2 = self.pers2
        ref = pers2.save({'name': 'Game1', 'designer': 1, 'artist': 2})
        ref_loaded = pers2.load_references(None, ref)
        self.assertEquals(ref_loaded, {'_refLoaded': True, 'designer': u'John',
                                       'name': u'Game1', 'artist': u'Julius',
                                       'id': 1})

    def tearDown(self):
        Alchemy.destroy()


class TestPersistenceAlchemyReferencesMany(unittest.TestCase):

    def setUp(self):
        field1 = FieldText('Name')

        schema = Schema('test', 'browser')
        schema.add_field(field1)
        self.pers = PersistenceAlchemy(schema, ':memory:')
        field2 = FieldRef('Designer', params={'ref': 'browser.name',
            'multiple': True})

        field1 = FieldText('Name')

        field3 = FieldRef('Artist', params={'ref': 'browser.name'})

        schema = Schema('test', 'designers')

        schema.add_field(field1)
        schema.add_field(field2)
        schema.add_field(field3)

        self.pers2 = PersistenceAlchemy(schema, ':memory:')
        self.pers2.all_created()

        self.pers.save({'name': 'John'})
        self.pers.save({'name': 'Julius'})

    def test_ref_multivalue(self):
        field2 = FieldRef('Designer',
                          multiple=True,
                          params={'ref': 'browser.name'})

        field1 = FieldText('Name')
        schema = Schema('test', 'boardgames')
        schema.add_field(field2)
        schema.add_field(field1)
        pers2 = PersistenceAlchemy(schema, ':memory:')
        pers2.all_created()
        board2 = pers2.save({'designer': [1, 2], 'name': 'Pilares'})
        obj = pers2.load_references([], board2)
        self.assertEquals(obj,
            {'designer': [u'John', u'Julius'],
            'name': u'Pilares', '_refLoaded': True, 'id': 1}
        )

    def tearDown(self):
        Alchemy.destroy()


if __name__ == '__main__':
    unittest.main()
