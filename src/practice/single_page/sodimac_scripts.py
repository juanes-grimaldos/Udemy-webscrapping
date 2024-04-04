import requests # pip install requests
from lxml import html # pip install lxml
import json

# USER AGENT PARA PROTEGERNOS DE BANEOS
headers = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
     " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
     "ZONE_NAME": "BOGOTA D.C.",
     "regionName_key": "CUNDINAMARCA",
     "municipal_name": "ZONA NORTE",
     "region":	"10",
     "usrLocation":	"10",
     "municipal":	"24677"
}

url = "https://www.homecenter.com.co/homecenter-co/search/?Ntt=Cemento%2050kg"

response = requests.get(url, headers=headers)
parsen = html.fromstring(response.text)

datos = parsen.xpath("//script[@id='__NEXT_DATA__']")
datos = datos[0].text_content()
objeto = json.loads(datos)
with open('data.json', 'w') as file:
    json.dump(objeto, file)
