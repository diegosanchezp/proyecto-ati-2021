import unittest
from .base_test import BaseSeleniumUnitTest
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestConfig(BaseSeleniumUnitTest):
  def setUp(self):
    super().setUp()
    self.page_url = "http://localhost:5000/configuracion"
  
  def test_config(self):
    # Test name: Config
    # Step # | name | target | value

    # Loguear al usuario
    self.login_user()

    # 1 | open | http://localhost:5000/configuracion | 
    self.driver.get(self.page_url)

    # 3 | click | id=notificaciones-comentarios | 
    self.driver.find_element(By.ID, "notificaciones-comentarios").click()

    # Guardar 4 | click | css=.btn-primary:nth-child(1) | 
    self.driver.find_element(By.ID, "guardar-config").click()

    # Después de hacer clicks en los checkbox  haber y hacer clic en guardar, se tiene que refrescado la página nuevamente
    self.assertEqual(self.driver.current_url, self.page_url)

    # Checkbox de notificaciones de comentarios no esta seleccionado
    self.assertFalse(self.driver.find_element(By.ID, "notificaciones-comentarios").is_selected())
  
if __name__ == '__main__':
    unittest.main()
