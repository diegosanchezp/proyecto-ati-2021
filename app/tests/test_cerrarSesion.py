import unittest
from .base_test import BaseSeleniumUnitTest
from selenium.webdriver.common.by import By

class TestCerrarSesion(BaseSeleniumUnitTest):
  """
  Usuario logueado pueda terminar sesión
  """

  def test_cerrarSesion(self):
    # Test name: Cerrar Sesion
    # Step # | name | target | value
    self.login_user()

    # 1 | open | http://localhost:5000/mural/1 |
    self.driver.get("http://localhost:5000/mural/1")

    # 3 | click | id=cerrar-sesion-boton |
    self.driver.find_element(By.ID, "cerrar-sesion-boton").click()

    # Se tiene que redireccionar hacia la vista del login
    self.assertEqual(self.driver.current_url, "http://localhost:5000/")
