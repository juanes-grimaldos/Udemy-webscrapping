import requests
import logging
import json
import random
from time import sleep
"""
En este script se hace una extracción de los datos del Servicio Nacional 
Civil para la contratación de un profesional universitario en el departamento
de Bogotá, Colombia. 
"""

logging.basicConfig(level=logging.INFO)

headers = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
  'Accept': 'application/javascript, application/json',
  'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
  'Accept-Encoding': 'gzip, deflate, br, identity',
  'X-Range': 'items=0-9',
  'Range': 'items=0-9',
  'Content-Type': 'application/x-www-form-urlencoded',
  'X-Requested-With': 'XMLHttpRequest',
  'DNT': '1',
  'Sec-GPC': '1',
  'Connection': 'keep-alive',
  'Referer': 'https://simo.cnsc.gov.co/',
  'Cookie': 'BIGipServerSimo=627353792.36895.0000; f5avraaaaaaaaaaaaaaaa_session_=NLFDEEPAEBKAOPEJGBIDGBEHJOHBIAJOLGGKLNPHHOGKCKENKCADPHHPAMJOKIGAPAHDBOFFGNKLCGJMIJJAJGFCNCDLJOMOANELKECCCIMECACJPMMOEEOFBHDLAKFP; f5avraaaaaaaaaaaaaaaa_session_=HIICEIMCKHADHCDKHKBNAEMOPGNNFKGMGOFOBIJJKCKDOHJMODBJKBCCAOPGEDOPGFBDDBMNIAPJBCGDKMFACGLBIDPHNGOHBPDCHNMBPGEONNCGJPLDBNFCLFIAIGJE',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin'
}

payload = {}

url_base = "https://simo.cnsc.gov.co/empleos/ofertaPublica/?"
search_bar = "search_palabraClave=profesional%20universitario&"
data = [{'ok':0}]
page = 0
output = []

while data:
    parm = ("search_convocatoria=&search_entidad=&"
            "search_departamento=6&search_nivel=3"
            "&search_salario=&search_municipio=144"
            f"&search_numeroOPEC=&page={page}&size=10")
    url = url_base + search_bar + parm

    response = requests.request("GET", url, headers=headers, data=payload)
    response.json()
    data = response.json()
    if data:
        loop_range = len(data)
        for i in range(loop_range):
            output.append({
                "id_opec": data[i]['id'],
                "job_tenure": data[i]['empleo']['requisitosMinimos'][0]['experiencia'],
                "academic_background": data[i]['empleo']['requisitosMinimos'][0]['estudio'],
                "company": data[i]['empleo']['convocatoria']['nombre'],
                "salary": data[i]['empleo']['asignacionSalarial'],
                "process_type": data[i]['empleo']['convocatoria']['tipoProceso']
            })

    else:
        # Store output as JSON file
        with open('output.json', 'w') as file:
            json.dump(output, file)
        break
    sleep_time = random.randint(1, 5)
    sleep(sleep_time)
    logging.info(f"Page {page} successfully scraped.")
    page += 1   
