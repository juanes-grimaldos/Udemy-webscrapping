from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv


# Asi podemos setear el user-agent en selenium
opts = Options()
opts.add_argument(
    "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
opts.add_argument("--headless") # Headless Mode: no se vea la ventana

# Instancio el driver de selenium que va a controlar el navegador
# A partir de este objeto voy a realizar el web scraping e interacciones
driver = webdriver.Chrome(
    service = Service(ChromeDriverManager().install()), 
    options = opts
)

driver.get('https://www.kayak.com.co/flights/BOG-TPA/2024-04-29/2024-05-06?'
           'sort=bestflight_a')

# TODO: Darle click cuantos vuelos haya en la base de datos

output = {}
item_reduction = [0]

for i in range(8):
    flight_list_count = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//div[@data-resultid]/"
             "div[contains(@class, 'pres-rounded')]")
        )
    )

    flight_list_count = [item for item in flight_list_count 
                         if item not in item_reduction]

    for flight in flight_list_count:
        id = flight.find_element(By.XPATH, "..").get_attribute("data-resultid")
        company = flight.find_element(
            By.XPATH, ".//div[contains(@class, 'provider-name')]").text
    
        price = flight.find_element(
            By.XPATH, ".//div[contains(@class, 'price-text-container')]"
            "/div[contains(@class, 'price-text')]").text
        
        price = float(price.replace('$', '').replace('.', ''))

        output[id] = {"company": company, "price": price}

    boton = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//div[contains(@class, 'show-more-button') and "
             "contains(@role, 'button')]")
        )
    )

    item_reduction = flight_list_count
    boton.click()



# Write the output to a CSV file
with open('output.csv', 'w', newline='') as csvfile:
    fieldnames = ['id', 'company', 'price']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    
    for id, data in output.items():
        writer.writerow(
            {'id': id, 'company': data['company'], 'price': data['price']}
        )