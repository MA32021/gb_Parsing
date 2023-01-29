# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Compose


def process_price(value):
    """
    Пред-обработчик цены - убираем лишние пробелы и забираем цену и валюту
    """
    if value:
        price = int(value[0].replace(' ', ''))
        currency = value[1].strip()
        return [{'price': price, 'currency': currency}]
    else:
        return value


def process_image_url(value: str):
    """
    Добавим баовый url к линку на картинку
    """
    return 'https://castorama.ru' + value


def clean_name(value: str):
    """
    Убираем обрамдяющие пробелы и перенос строки
    """
    return value.replace('\n', '').strip()


def process_specs_list(value: str):
    """
    Убираем обрамдяющие пробелы и перенос строки
    """
    return value.replace('\n', '').strip()


def process_specs_vals(value: str):
    """
    Убираем обрамдяющие пробелы и перенос строки
    """
    return value.replace('\n', '').strip()


class AdsParserItem(scrapy.Item):
    name = scrapy.Field(input_processor=MapCompose(clean_name), output_processor=TakeFirst())
    price = scrapy.Field(input_processor=Compose(process_price), output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=MapCompose(process_image_url))
    url = scrapy.Field(output_processor=TakeFirst())
    specs = scrapy.Field(input_processor=MapCompose(process_specs_list))
    spec_vals = scrapy.Field(input_processor=MapCompose(process_specs_vals))
    _id = scrapy.Field()
