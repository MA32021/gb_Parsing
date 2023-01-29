import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import HtmlResponse
from ads_parser.items import AdsParserItem
from scrapy.loader import ItemLoader
from scrapy.linkextractors import LinkExtractor

# Наследуем паука от CrawlSpider, чтобы обойти все страницы товаров по правилам
class CastoramaSpider(CrawlSpider):
    name = 'castorama'
    allowed_domains = ['castorama.ru']
    rules = (
        # Правило для страницы с конкретным товаром - передаем в парсер parse_ads
        Rule(LinkExtractor(restrict_xpaths='//a[@class="product-card__img-link"]'), callback='parse_ads'),
        # Правило для страницы с каталогом - продолжаем обход
        Rule(LinkExtractor(restrict_xpaths='//div[@class ="pages"]'), follow=True)
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # закомментируем для выполнения в блокноте
        #self.keyword = kwargs.get("search")
        self.keyword = 'генератор'
        self.start_urls = [f'https://www.castorama.ru/catalogsearch/result/?q={self.keyword}/']

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=AdsParserItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price', '//span[@class="price"]/span/span/text()')
        loader.add_xpath('photos','//span[@itemprop="image"]/@content')
        # спарсим характеристики товара предварительно в отдельные поля specs и spec_vals
        loader.add_xpath('specs', '//span[@class="specs-table__attribute-name "]/text()')
        loader.add_xpath('spec_vals', '//dd[@class="specs-table__attribute-value _first"]/text()')
        loader.add_value('url', response.url)
        yield loader.load_item()
