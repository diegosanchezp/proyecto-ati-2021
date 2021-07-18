import unittest
from app import create_app
from dotenv import load_dotenv

class TestApp(unittest.TestCase):
    def setUp(self):
        """
        Fixtures
        """
        load_dotenv()
        self.app = create_app(config_class="TestingConfig")

    def test_app_is_created(self):
        """
        Verificar que la app de flask sea creada
        """
        self.assertIsNotNone(self.app)

    def test_app_is_testconfigured(self):
        """
        Verificar que la app de flask este en modo test
        """
        self.assertTrue(self.app.testing)

if __name__ == '__main__':
    unittest.main()
