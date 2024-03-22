import requests
from bs4 import BeautifulSoup
import csv 

"""
OBJETIVO:
    - Extraer los precios de los colchones de la pagina principal de Colchones Amore
CREADO POR: JUANES GRIMALDOS
"""
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
}


url = 'https://www.colchonesamore.com/tiendaenlinea' # URL Semilla

# Hacemos el requerimiento a la web
respuesta = requests.get(url, headers=headers)

# Verificamos que obtenemos codigo 200
print(respuesta)

# Cargamos el arbol HTML en beautifoul soup
soup = BeautifulSoup(respuesta.text, 'lxml')

# Obtenemos todas las noticias
f = open('precios_colchones_amore.csv', 'w')
write_machine = csv.writer(f)

results = {}

item_list = soup.find_all('h3', attrs={'data-hook': 'product-item-name'})

price_list = soup.find_all('span',  attrs={'data-hook': "price-range-from"})

for item, price in zip(item_list, price_list):
    item_str = item.text.strip()
    price_str = price.text.replace('Desde $', '').replace('.', '').replace(',', '.').strip()  # Clean price text
    price_num = float(price_str)  # Convert price to a float
    results[item_str] = price_num  # Add the item-price pair to the dictionary
    write_machine.writerow([item_str, price_str])

f.close()