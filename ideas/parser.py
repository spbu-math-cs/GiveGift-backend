from typing import Optional, List, Any
import requests


def get_link(name_of_product, min_budget, max_budget) -> str:
    # noinspection IncorrectFormatting
    return 'https://search.wb.ru/' \
           f'exactmatch/ru/common/v4/search?appType=1&curr=rub&dest=-1257786&priceU={min_budget}00;' \
           f'{max_budget}00&page=1&query={name_of_product}&resultset=catalog&sort=popular&spp=24&' \
           'suppressSpellcheck=false'


def get_query_link(name_of_product, min_budget, max_budget):
    response = requests.get(
        get_link(name_of_product=name_of_product, min_budget=min_budget, max_budget=max_budget)
    )
    return response.json()


def get_id_and_name(response, adult):
    # noinspection PyBroadException
    try:
        if adult == True:
            print(response['data']['products'][0]['name'])
            return [response['data']['products'][0]['id'], response['data']['products'][0]['name']]
        else:
            for product in response['data']['products']:
                if 'isAdult' not in product:
                    return [product['id'], product['name']]
    except:
        print('No products found')
        pass


# noinspection PyBroadException
def get_image_link(product_id):
    try:
        _shot_id = product_id // 100000
        _short_id = product_id // 100000
        """Используем match/case для определения basket на основе _short_id"""
        if 0 <= _short_id <= 143:
            basket = '01'
        elif 144 <= _short_id <= 287:
            basket = '02'
        elif 288 <= _short_id <= 431:
            basket = '03'
        elif 432 <= _short_id <= 719:
            basket = '04'
        elif 720 <= _short_id <= 1007:
            basket = '05'
        elif 1008 <= _short_id <= 1061:
            basket = '06'
        elif 1062 <= _short_id <= 1115:
            basket = '07'
        elif 1116 <= _short_id <= 1169:
            basket = '08'
        elif 1170 <= _short_id <= 1313:
            basket = '09'
        elif 1314 <= _short_id <= 1601:
            basket = '10'
        elif 1602 <= _short_id <= 1655:
            basket = '11'
        elif 1656 <= _short_id <= 1919:
            basket = '12'
        else:
            basket = '13'
        url = f"https://basket-{basket}.wb.ru/vol{_shot_id}/part{product_id // 1000}/{product_id}/images/big/1.jpg"
        return url
    except:
        pass


# noinspection PyBroadException
def get_image_link_or_none(product_name: str, min_budget: int, max_budget: int, adult: bool):
    try:
        id_and_name = get_id_and_name(get_query_link(product_name, min_budget, max_budget), adult)
        return [get_image_link(id_and_name[0]), id_and_name[1]]
    except:
        pass
    return [None, None]
