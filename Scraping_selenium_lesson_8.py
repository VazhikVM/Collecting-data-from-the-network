from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from time import sleep

options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'

service = Service(r'geckodriver.exe')
driver = webdriver.Firefox(service=service, options=options)

# driver = webdriver.Firefox(executable_path=r'geckodriver.exe', options=options)
driver.get('https://scrapingclub.com/exercise/basic_login/')

WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.XPATH, "//input[@id='id_name']")))

# Добавить ожидание
login = driver.find_element(by=By.XPATH, value="//input[@id='id_name']")
login.send_keys('scrapingclub')


sleep(5)



driver.quit()
