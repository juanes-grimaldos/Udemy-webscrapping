import requests
import logging
import random
from time import sleep
import sqlite3
import json

"""
En este script se hace una extracción de los datos del Servicio Nacional 
Civil para LOS RESULTADOS DE LA PRUEBA DE SIMO
"""
logging.basicConfig(level=logging.INFO)


url_base = "https://simo.cnsc.gov.co/publicaevaluaprueba/833869410?"
payload = {}
# TODO: toca actualizar estos headers antes de ejecutar el script
headers = {
  'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
  'X-Range': 'items=10-19',
  'Range': 'items=10-19',
  'Content-Type': 'application/x-www-form-urlencoded',
  'X-Requested-With': 'XMLHttpRequest',
  'Referer': 'https://simo.cnsc.gov.co/',
  'Cookie': 'f5avraaaaaaaaaaaaaaaa_session_=MMLIIIMNEKADJKFMPINPECFKAGEPDLKDKPICKGLLONEBGKJLDAOLBJLEEPOLJLLDKLIDDJMICLJKOMKHHBEACAJCFAMMFMDLPADKGOFEMKFCEOJEMNIOGDDLDBGNNBOE; _ga=GA1.3.1348282772.1720150360; _ga_B463KWF6H4=GS1.3.1725037912.10.1.1725041808.0.0.0; _fbp=fb.2.1720713568569.54058010288668240; _ga_H2KN1DDY4N=GS1.3.1721950905.2.1.1721950923.0.0.0; BIGipServerSimo=660908224.36895.0000; JSESSIONID=4292FDF481D0D8A167065FF47839D81A; FCK_NmSp=simo%3Adocumentos%3Amanual_ciudadano; BIGipServerwiki_80=493136064.20480.0000; FCK_NmSp_acl=o5gcabkedtiihfhse3f2fm8ig4; FCK_SCAYT_AUTO=on; f5avraaaaaaaaaaaaaaaa_session_=EPCAFDAOPPCOMKFPAHFIJAKHMLOJBNAGGGJLKOHELAEOACOEOOPLCKEMKDFMAPDGIOODBMJAPLNBDIEKCCDAFABCCAGIHMINKAHEOOIKOMIPOGKMKFHNPLJKOOHONLOB; _gid=GA1.3.260695022.1725037913; _gat=1',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'Priority': 'u=0'
}

data = [{'ok':0}]
page = 0
output = []

while data:
    search_params = f"page={page}&size=10"
    url = url_base + search_params

    response = requests.request("GET", url, headers=headers, data=payload)
    try:
        response.json()
        data = response.json()
        loop_range = len(data)
        for i in range(loop_range):
            output.append({
                "id": data[i]['id'],
                "aprobo": data[i]['evaluaPrueba']['aprobo'],
            })
    
    except json.JSONDecodeError as e:
        # en este caso se ha llegado al final de la paginación y solo hay un 
        # registro en la respuesta
        search_params = f"page={page}&size=1"
        url = url_base + search_params
        response = requests.request("GET", url, headers=headers, data=payload)
        loop_range = len(data)
        for i in range(loop_range):
            output.append({
                "id": data[i]['id'],
                "aprobo": data[i]['evaluaPrueba']['aprobo'],
            })

        logging.info("No more data to extract")
        
        # Store output in SQLite database

        conn = sqlite3.connect('output.db')
        c = conn.cursor()

        # Create table
        c.execute('''CREATE TABLE IF NOT EXISTS vrm_data
             (id INTEGER, aprobo INTEGER)''')

        # Insert data into table
        for item in output:
            c.execute("INSERT INTO vrm_data (id, aprobo) VALUES (?, ?)",
                  (item['id'], item['aprobo']))

        # Commit changes and close connection
        conn.commit()
        conn.close()
        break

    sleep_time = random.randint(1, 5)
    sleep(sleep_time)
    logging.info(f"Page {page} successfully scraped.")
    page += 1   
