from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from time import sleep
from random import randint
import sqlite3

con = sqlite3.connect('clothes.db')
cursor = con.cursor()
cursor.execute('''create table if not exists clothes (
    img TEXT,
    link text,
    title text,
    price text)''')
con.commit()


def insert_sqlite3(data, table):
    """
    data - Передаем список словарей (список словарей)
    table - Название таблицы (строка)
    """
    cursor.executemany(
        f'''insert into {table} {tuple(data[0].keys())}
    values(
        ?, ?, ?, ?
    )
    ''', [tuple(i.values()) for i in data])
    con.commit()
    print('insert_successfully')


# Логинимся

options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'

service = Service(r'geckodriver.exe')
driver = webdriver.Firefox(service=service, options=options)
driver.get('https://scrapingclub.com/exercise/basic_login/')
# html = driver.page_source если нужно получить html страницы
WebDriverWait(driver, 30).until(ec.presence_of_element_located((By.XPATH, "//input[@id='id_name']")))

login = driver.find_element(by=By.XPATH, value="//input[@id='id_name']")
password = driver.find_element(by=By.ID, value="id_password")
login.send_keys('scrapingclub')
password.send_keys('scrapingclub')

driver.find_element(by=By.XPATH, value="//button[contains(text(), 'Log in')]").click()

sleep(2)

driver.get('https://scrapingclub.com/exercise/list_infinite_scroll/')

first_heigth = driver.execute_script('return document.body.scrollHeight')
sleep(randint(2, 5))
print(f'Первая высота = {first_heigth}')

while True:
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    sleep(randint(2, 5))

    new_heigth = driver.execute_script('return document.body.scrollHeight')
    print(f'Новая высота = {first_heigth}')

    if first_heigth == new_heigth:
        print(f"Конец скролла {first_heigth}")
        break

    first_heigth = new_heigth

cards = driver.find_elements(by=By.XPATH, value='//div[@class="card"]')

print(len(cards))

for card in cards:
    temp_dict = [{
        'img': 'https://scrapingclub.com/' + card.find_element(by=By.XPATH, value='.//img').get_attribute('src'),
        'link': 'https://scrapingclub.com/' + card.find_element(by=By.XPATH, value='.//a').get_attribute('href'),
        'title': card.find_element(by=By.XPATH, value='.//h4[@class="card-title"]/a').text,
        'price': card.find_element(by=By.XPATH, value='.//div[@class="card-body"]/h5').text
    }, ]
    # print(img)
    insert_sqlite3(temp_dict, 'clothes')

driver.quit()
