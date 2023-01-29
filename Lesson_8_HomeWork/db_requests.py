from pymongo import MongoClient
from pprint import pprint


def find_by_parameter(parameter='', value=''):
    if not parameter:
        return []
    client = MongoClient('localhost', 27017)
    db = client.castorama
    db.list_collection_names()
    collection_shop = db.castorama
    return list(collection_shop.find({parameter:value}))

if __name__ == '__main__':
    param = input('Введите параметр поиска: ')
    val = input('Введите значение: ')
    pprint(find_by_parameter(parameter=param, value=val))