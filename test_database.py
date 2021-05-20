import unittest
import database as db

class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        db.DB_NAME = ":memory:"

    def setUp(self):
        with open("modelo.sql") as script:
            connection = db.sqlite3.connect(db.DB_NAME)
            connection.executescript(script.read())
            connection.close()

    def test_new_user(self):
        db.nuevo_usuario("user1", "123456")
        self.assertEqual('foo'.upper(), 'FOO')

    def test_new_user2(self):
        db.nuevo_usuario("user1", "123456")
        self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
    unittest.main()