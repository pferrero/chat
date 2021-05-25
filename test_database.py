import unittest
import database as db

class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        db.DB_NAME = "test_database.db"

    def setUp(self):
        with open("modelotest.sql") as script:
            connection = db.sqlite3.connect(db.DB_NAME)
            connection.executescript(script.read())
            connection.close()

    def tearDown(self):
        connection = db.sqlite3.connect(db.DB_NAME)
        with connection:
            connection.execute("DROP TABLE IF EXISTS mensaje")
            connection.execute("DROP TABLE IF EXISTS usuario")

    def test_exists_user(self):
        db.nuevo_usuario("user5", "123456")
        self.assertTrue(db.exists_user("user5"))

    def test_new_user(self):
        db.nuevo_usuario("user5", "123456")
        connection = db.sqlite3.connect(db.DB_NAME)
        cur = connection.cursor()
        cur.execute("SELECT username, pass FROM usuario \
                    WHERE username = 'user5'")
        user = cur.fetchone()
        connection.close()
        self.assertEqual(user, ("user5", "123456"))

    def test_create_message(self):
        db.crear_mensaje("user1", "user2", "test")
        connection = db.sqlite3.connect(db.DB_NAME)
        cur = connection.cursor()
        cur.execute("SELECT * FROM mensaje WHERE msj = 'test'")
        msj = cur.fetchone()
        connection.close()
        # None = not found
        self.assertIsNotNone(msj)

    def test_get_all_messages_empty(self):
        messages = db.get_mensajes("user2", "user3")
        self.assertTrue(len(messages) == 0)

    def test_get_all_messages(self):
        messages = db.get_mensajes("user1", "user2")
        self.assertTrue(len(messages) == 5)

    def test_get_messages_fromto_empty(self):
        messages = db.get_mensajes_from_to("user3", "user4")
        self.assertTrue(len(messages) == 0)

    def test_get_messages_fromto(self):
        messages = db.get_mensajes_from_to("user2", "user1")
        self.assertTrue(len(messages) == 2)


if __name__ == '__main__':
    unittest.main()