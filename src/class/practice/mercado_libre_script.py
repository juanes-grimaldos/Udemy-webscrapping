from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess

class InfoML(Item):
    id = Field()
    item = Field()
    price = Field()

# CLASE CORE - SPIDER
class KayakSpider(Spider):
    name = "MercadoLibreScripy" # nombre, puede ser cualquiera 
    
    # Forma de configurar el USER AGENT en scrapy
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }    

    # URL SEMILLA
    start_urls = ['https://listado.mercadolibre.com.co/computadores#D[A:computadores]']


    
    def parse(self, response):
        sel = Selector(response) 
        computers = sel.xpath(".//div[@class='ui-search-result__content-wrapper']")
        i = 0
        for i, computer in enumerate(computers):
            item = ItemLoader(InfoML(), computer)
            item.add_value('id', i)
            item.add_xpath('item', ".//h2[@class='ui-search-item__title']/text()")
            item.add_xpath('price', ".//span[@class='andes-money-amount ui-search-price__part ui-search-price__part--medium andes-money-amount--cents-superscript']//span[@class='andes-money-amount__fraction']/text()")
            yield item.load_item()


# EJECUCION EN TERMINAL:
# scrapy runspider class/practice/mercado_libre_script.py -o resultados.csv


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(KayakSpider)
    process.start()
