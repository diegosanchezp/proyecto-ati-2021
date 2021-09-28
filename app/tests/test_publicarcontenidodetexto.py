# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestUCPublicarcontenidodetexto():
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_uCPublicarcontenidodetexto(self):
    self.driver.get("http://localhost:5000/")
    self.driver.set_window_size(1278, 727)
    self.driver.find_element(By.ID, "email").click()
    self.driver.find_element(By.ID, "email").send_keys("cesar@cesar.com")
    self.driver.find_element(By.ID, "password").click()
    self.driver.find_element(By.ID, "password").send_keys("123Qwe")
    self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
    self.driver.find_element(By.LINK_TEXT, "See my profile").click()
    self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(2) > .btn").click()
    self.driver.find_element(By.ID, "contenido").click()
    self.driver.find_element(By.ID, "contenido").send_keys("Publicacion Automatizada")
    self.driver.find_element(By.ID, "tipo_publicacion").click()
    dropdown = self.driver.find_element(By.ID, "tipo_publicacion")
    dropdown.find_element(By.XPATH, "//option[. = 'Publica']").click()
    self.driver.find_element(By.ID, "publicar").click()
  
