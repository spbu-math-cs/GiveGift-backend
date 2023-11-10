import requests

def queryLink(name,min_budg,max_budg):
    response = requests.get(
        f'https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1&curr=rub&dest=-1257786&priceU={min_budg}00;{max_budg}00&page=1&query={name}&resultset=catalog&sort=popular&spp=24&suppressSpellcheck=false',
    )
    return response.json()
