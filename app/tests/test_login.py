import unittest
from .base_test import BaseSeleniumUnitTest

class TestLogin(BaseSeleniumUnitTest):

    def test_login(self):
        """
        Loguear un usuario registrado en el sistema
        """

        self.login_user()

        # Se tiene que redireccionar al mural
        self.assertEqual(self.driver.current_url, "http://localhost:5000/mural/1")

if __name__ == '__main__':
    unittest.main()
