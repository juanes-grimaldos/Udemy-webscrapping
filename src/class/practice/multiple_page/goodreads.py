from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.crawler import CrawlerProcess


class GoodreadsItem(Item):
    title = Field()
    author = Field()
    rating = Field()
    num_pages = Field()

class GoodreadsSpider(CrawlSpider):
    name = 'goodreads'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 20
    }
    allowed_domains = ['goodreads.com']

    start_urls = ['https://www.goodreads.com/search?q=adventure&qid=']

    download_delay = 2

    rules = (
        Rule( # REGLA #1 => HORIZONTALIDAD POR PAGINACION
            LinkExtractor(
                allow=r'/page=\d+' # Patron en donde se utiliza "\d+", expresion que puede tomar el valor de cualquier combinacion de numeros
            ), follow=True),
        Rule( # Regla de movimiento VERTICAL hacia el detalle de los hoteles
            LinkExtractor(
                allow=r'/book/show/' # Si la URL contiene este patron, haz un requerimiento a esa URL
            ), follow=True, callback="parse_reads"), # El callback es el nombre de la funcion que se va a llamar con la respuesta al requerimiento hacia estas URLs
    )

    def parse_reads(self, response):
        sel = Selector(response)

        item = ItemLoader(GoodreadsItem(), sel)
        item.add_xpath('title', './/h1[@data-testid="bookTitle"]/text()')
        item.add_xpath('author', './/h3[@class="Text Text__title3 Text__regular"]//span[@class="ContributorLink__name"]/text()')
        item.add_xpath('rating', './/a[@class="RatingStatistics RatingStatistics__interactive RatingStatistics__centerAlign"]//div[@class="RatingStatistics__rating"]/text()')
        item.add_xpath('num_pages', './/p[@data-testid="pagesFormat"]/text()')

        yield item.load_item()

if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(GoodreadsSpider)
    process.start()

# EJECUCION
# scrapy runspider class\practice\multiple_page\goodreads.py -o goodreads.json