import unittest
from engine.persistence import PersistenceDict
from mocks import boardgames


class TestPersistence(unittest.TestCase):

    def setUp(self):
        self.manager = PersistenceDict('demo', 'boardgames',
                data=boardgames)

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
        self.assertEqual(items[0]['name'], 'The Pillars of the Earth')
        self.assertEqual(items[1]['name'], 'Coney Island')

if __name__ == '__main__':
    unittest.main()
