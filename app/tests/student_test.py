import unittest
from app.models.user import User
class StudentModelTestCase(unittest.TestCase):
    def setUp(self):
        self.user = User(nombre="María Paula Herrero")

    def test_username_is_lowercase(self):
        """
        Dado nombre real de un posible usuario,
        Verificar que el nombre de usuario aka "username" este
        en lowercase y espacios en blanco reemplazados por _
        """

        self.assertEqual(self.user.username, "maría_paula_herrero")

    def test_username_is_notnone(self):
        """
        Dado nombre real de un posible usuario
        Verificar que el nombre de usuario aka "username" se crea
        a partir del nombre real
        """
        self.assertIsNotNone(self.user.username)

if __name__ == '__main__':
    unittest.main()
