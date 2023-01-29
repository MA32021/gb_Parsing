# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
import hashlib
from urllib.parse import urlparse

import scrapy
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes


class AdsParserPipeline:
    def __init__(self):
        # Инициализируем mongo
        client = MongoClient('localhost', 27017)
        self.mongobase = client.castorama

    def process_item(self, item, spider):
        # сохраним item в mongo
        collection = self.mongobase[spider.name]
        # добавим поисковое слово в поле keyword
        db_record = {
            'keyword': spider.keyword,
            'name': item.get('name'),
            'price': item.get('price'),
            'photos': item.get('photos'),
            'url': item.get('url'),
            # соберем спецификации товара из полей specs и spec_vals в словарь:
            'specifications': dict(zip(item.get('specs'), item.get('spec_vals')))
        }
        collection.insert_one(db_record)
        return item

'''
Чтобы скавчивались картинки должен быть установлен модуль pillow
В settings.py надо установить параметер IMAGES_STORE
'''

class AdsPhotosPipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None, *, item=None):
        '''
        Переопределим file_path чтобы добавить в имя файла подпапку для товара из url
        '''
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        sub_folder = urlparse(url=item.get('url')).path
        return f'full{sub_folder}{image_guid}.jpg'

    def get_media_requests(self, item, info):
        if item.get('photos'):
            for img in item.get('photos'):
                print(img)
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        '''
        Метод вызывается в конце обработки item
        :param results: здесь лежит список, элементами которого являются кортежи
        по количеству скачанных картинок: на первом месте True/False - успешность загрузки,
        на втором - checksum, path, status (downloaded или uptodate ) и url
        '''
        if results:
            # добавим все из results в поле photos нашего item -
            # вместо ссылки на картинку в этом поле будет словарь из results (элемент 1 кортежа)
            # для тех кортежей, где элемент 0 равн True, что означает успешную загрузку:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
