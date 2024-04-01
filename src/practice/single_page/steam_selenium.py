from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
"""
Este es un ejemplo de web scraping con Selenium en la página de Steam

En este ejemplo vemos como extraer los precios e interactuar con el eje
Y para obtener más resultados.
"""
# TODO: agregar paginación para obtener requerimientos del sistema y comentarios

opts = Options()
opts.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
opts.add_argument("--headless")

driver = webdriver.Chrome(
    service = Service(ChromeDriverManager().install()), 
    options = opts
)


def scroll_smooth(driver, i, scroll_multiplayer):
    """
    scrolling function to go down the page and load more games
    :param driver: selenium driver
    :param i: iteration number
    :param scroll_multiplayer: how many times pixels are going to be scrolled
    """
    scroll_to = 2000 * (i + 1)
    start = (i * 2000) 
    for number in range(start,  scroll_to, scroll_multiplayer):
        scrollingScript = f""" 
          window.scrollTo(0, {number})
        """
        driver.execute_script(scrollingScript)


driver.get(
    'https://store.steampowered.com/search/?term=shooter'
    '&category1=998&hidef2p=1&ndl=1'
)

sleep(10)


output = {}
item_reduction = [0]
max_scroll = 20

for i in range(max_scroll):
    scroll_smooth(driver, i, 20)

    games_list = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//div[@id='search_resultsRows']/a")
        )
    )

    games_list = [item for item in games_list if item not in item_reduction]

    for game in games_list:
        title = game.find_element(
            By.XPATH, ".//span[@class='title']").text    
        try:
            price = game.find_element(
            By.XPATH, ".//div[@class='discount_final_price']"
            ).text
            price = price.replace('COL$', '').replace('.', '')
            price = float(price.replace(',00','').strip())
        except:
            price = 0.0
        logging.info(f'{title} - {price}')
        output[title] = price
    
    item_reduction = games_list

with open('output_stream.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['title', 'price']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for title, price in output.items():
        writer.writerow(
            {'title': title, 'price': price}
        )