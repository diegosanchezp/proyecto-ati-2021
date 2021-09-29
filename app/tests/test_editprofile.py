# Generated by Selenium IDE
import unittest, os
from .base_test import BaseSeleniumUnitTest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestEditprofile(BaseSeleniumUnitTest):
  
  def test_editprofile(self):

    self.driver.get("http://localhost:5000/")
    # 3 | click | id=email | 
    self.driver.find_element(By.ID, "email").click()
    # 4 | type | id=email | diego@mail.com
    self.driver.find_element(By.ID, "email").send_keys("diego@mail.com")
    # 5 | type | id=password | Dev123456
    self.driver.find_element(By.ID, "password").send_keys("Dev123456")
    # 6 | click | css=.btn-primary | 
    self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()

    # Test name: edit-profile
    # Step # | name | target | value
    # 1 | open | /mural/1 | 
    self.driver.get("http://localhost:5000/mural/1")
    # 3 | click | linkText=Ver mi perfil | 
    self.driver.find_element(By.ID, "ver-mi-perfil-boton").click()
    # 4 | click | css=a:nth-child(1) > .btn-primary | 
    self.driver.find_element(By.CSS_SELECTOR, "a:nth-child(1) > .btn-primary").click()
    # 6 | type | id=nombre_foto | C:\fakepath\tonos.jpg

    #subir foto de perfil, prestar atencion a que imagen se sube para copiar su path y compararlo aqui
    #upload="/app/static/img/tonos.jpg"
    #self.driver.find_element(By.ID, "nombre_foto").send_keys(os.getcwd()+upload)

    self.driver.find_element(By.ID, "color").click()
    # 6 | type | id=color | Azul 
    self.driver.find_element(By.ID, "color").send_keys("Azul")
    # 7 | click | id=libro | 
    self.driver.find_element(By.ID, "libro").click()
    # 8 | type | id=libro | TLOR
    self.driver.find_element(By.ID, "libro").send_keys("TLOR")
    # 9 | click | id=musica | 
    self.driver.find_element(By.ID, "musica").click()
    # 10 | type | id=musica | Pop
    self.driver.find_element(By.ID, "musica").send_keys("Pop")
    # 11 | click | id=lenguajes_programacion | 
    self.driver.find_element(By.ID, "lenguajes_programacion").click()
    # 12 | type | id=lenguajes_programacion | PhP, Ruby
    self.driver.find_element(By.ID, "lenguajes_programacion").send_keys("PhP, Ruby")
    # 13 | click | id=video_juegos | 
    self.driver.find_element(By.ID, "video_juegos").click()
    # 14 | type | id=video_juegos | TLOU II, Sekiro
    self.driver.find_element(By.ID, "video_juegos").send_keys("Geometry dash")
    # 15 | click | id=descripcion | 
    self.driver.find_element(By.ID, "descripcion").click()
    # 16 | type | id=descripcion | Soy un estudiante
    self.driver.find_element(By.ID, "descripcion").send_keys("Soy un estudiante")
    # 18 | click | css=.col > .btn-primary | 
    self.driver.find_element(By.ID, "actualizar-perfil-boton").click()
    # 19 | click | linkText=Ver mi perfil | 
    self.driver.find_element(By.ID, "ver-mi-perfil-boton").click()

    


    self.assertEqual(self.driver.current_url, "http://localhost:5000/ver-perfil/diego_sanchez")

    self.assertEqual(self.driver.find_element(By.ID, "color").text , "Azul")

    self.assertEqual(self.driver.find_element(By.ID, "book").text , "TLOR")    

    self.assertEqual(self.driver.find_element(By.ID, "music").text , "Pop")

    self.assertEqual(self.driver.find_element(By.ID, "email").text , "diego@mail.com")
    
    self.assertEqual(self.driver.find_element(By.ID, "genre").text , "Masculino")

    self.assertEqual(self.driver.find_element(By.ID, "description").text , "Soy un estudiante")

    self.assertEqual(self.driver.find_element(By.ID, "video_games").text , "Geometry dash")

    self.assertEqual(self.driver.find_element(By.ID, "programming_languages").text , "PhP, Ruby")

    self.assertEqual(self.driver.find_element(By.ID, "id").text , "134423")

    self.assertEqual(self.driver.find_element(By.ID, "birthday").text , "11/02/3344")

    #comprobar foto de perfil
    #self.assertEqual(self.driver.find_element(By.ID, "main-profile-pic").get_attribute('src') , "http://localhost:5000/media/foto_perfil/615108d38064bb1b82d7760c")


    self.driver.quit()
  
if __name__ == '__main__':
    unittest.main()