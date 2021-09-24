import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestLogin(unittest.TestCase):
    def setUp(self):
        options = webdriver.FirefoxOptions()
        options.headless = True # No abrir una ventana del navegador
        self.driver = webdriver.Firefox(options=options)

    def tearDown(self):
        self.driver.quit()

    def test_login(self):
        """
        Loguear un usuario registrado en el sistema
        """

        # Test name: Login
        # Step # | name | target | value
        # 1 | open | http://localhost:5000/ | 
        self.driver.get("http://localhost:5000/")

        # 3 | type | id=email | aaron@mail.com
        self.driver.find_element(By.ID, "email").send_keys("aaron@mail.com")

        # 6 | doubleClick | id=password | 
        element = self.driver.find_element(By.ID, "password")
        actions = ActionChains(self.driver)
        actions.double_click(element).perform()

        # 7 | type | id=password | Dev123456
        self.driver.find_element(By.ID, "password").send_keys("Dev123456")

        # 8 | click | id=remember_me | 
        self.driver.find_element(By.ID, "remember_me").click()

        # 9 | click | css=.btn-primary | 
        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()

        # Se tiene que redireccionar al mural
        self.assertEqual(self.driver.current_url, "http://localhost:5000/mural/1")
