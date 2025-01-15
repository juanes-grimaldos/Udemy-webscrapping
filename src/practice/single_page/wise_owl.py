import requests
from bs4 import BeautifulSoup
import csv
from utils.fuctions import store_product_info


headers = {
    "User-Agent": 
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
}


url = 'https://www.wiseowl.co.uk/power-bi/exercises/dax/'

# Hacemos el requerimiento a la web
respuesta = requests.get(url, headers=headers)

# Cargamos el arbol HTML en beautifoul soup
soup = BeautifulSoup(respuesta.text, 'lxml')

results = {}
index = 0

item_list = soup.find_all(
    'panel-grid-item', 
    attrs={"class":"ExercisePanel"}
)

for item in item_list:
    index += 1
    title = item.findNext('td', string='Exercise:').findNext('td').text
    level = item.findNext('td', string='Level:').findNext('td').text
    topic = item.findNext('td', string='Topic:').findNext('a').text
    link = item.findNext('a', attrs={"title": "Show this exercise"}).get('href')
    hyperlink = f'https://www.wiseowl.co.uk{link}'
    results = {
        'index': index,
        'title': title,
        'level': level,
        'topic': topic,
        'link': hyperlink
    }
    store_product_info('wise_owl.json', results)
