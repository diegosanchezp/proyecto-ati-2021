import unittest
from .base_test import BaseSeleniumUnitTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestRegistrar(BaseSeleniumUnitTest):
  
  def test_registrar(self):
    """
    Registrar usuario diego_sanchez, este no tiene que estar
    registrado en base de datos para que el test pase
    """
    # Test name: Registrar
    # Step # | name | target | value
    # 1 | open | http://localhost:5000/registro | 
    self.driver.get("http://localhost:5000/registro")
    # 3 | click | id=nombre | 
    self.driver.find_element(By.ID, "nombre").click()
    # 4 | type | id=nombre | Diego Sanchez
    self.driver.find_element(By.ID, "nombre").send_keys("Diego Sanchez")
    # 5 | click | id=ci | 
    self.driver.find_element(By.ID, "ci").click()
    # 6 | type | id=ci | 27989123
    self.driver.find_element(By.ID, "ci").send_keys("26334929")
    # 7 | click | id=email | 
    self.driver.find_element(By.ID, "email").click()
    # 8 | type | id=email | diego@mail.com
    self.driver.find_element(By.ID, "email").send_keys("diego@mail.com")
    # 9 | click | id=fecha_nacimiento | 
    self.driver.find_element(By.ID, "fecha_nacimiento").click()
    # 10 | type | id=fecha_nacimiento | 2021-09-08
    self.driver.find_element(By.ID, "fecha_nacimiento").send_keys("2021-09-08")
    # 11 | click | id=fecha_nacimiento | 
    self.driver.find_element(By.ID, "fecha_nacimiento").click()
    # 12 | type | id=fecha_nacimiento | 0001-09-08
    self.driver.find_element(By.ID, "fecha_nacimiento").send_keys("0001-09-08")
    # 13 | type | id=fecha_nacimiento | 0019-09-08
    self.driver.find_element(By.ID, "fecha_nacimiento").send_keys("0019-09-08")
    # 14 | type | id=fecha_nacimiento | 0197-09-08
    self.driver.find_element(By.ID, "fecha_nacimiento").send_keys("0197-09-08")
    # 15 | type | id=fecha_nacimiento | 1978-09-08
    self.driver.find_element(By.ID, "fecha_nacimiento").send_keys("1978-09-08")
    # 16 | click | id=password | 
    self.driver.find_element(By.ID, "password").click()
    # 17 | type | id=password | Dev123456
    self.driver.find_element(By.ID, "password").send_keys("Dev123456")
    # 18 | click | id=retype_password | 
    self.driver.find_element(By.ID, "retype_password").click()
    # 19 | type | id=retype_password | Dev123456
    self.driver.find_element(By.ID, "retype_password").send_keys("Dev123456")
    # 20 | click | id=boton-registrar | 
    self.driver.find_element(By.ID, "boton-registrar").click()
  
    
    # Se tiene que redireccionar al mural
    self.assertEqual(self.driver.current_url, "http://localhost:5000/mural/1")
