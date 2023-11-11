# import openai
# import requests
# from flask import Flask, request, jsonify
# from bs4 import BeautifulSoup
#
#
# url = 'https://megamarket.ru/catalog/?q=картошка'
# response = requests.get(url)
# print(response.status_code)
# images = []
#
# soup = BeautifulSoup(response.text, features="html.parser")
# print(soup) #
# img_tag = soup.find('img')
# print(img_tag)
# if img_tag:
#         # Извлекаем ссылку на фотографию из атрибута src
#     photo_url = img_tag['src']
#     print("Ссылка на первую фотографию:", photo_url)
# else:
#     print("Фотографии не найдены на странице.")
# #print(images)
import requests
import requests_html
from requests import Response
# import requests
# from urllib.parse import urlencode
#
# url = "https://main-cdn.sbermegamarket.ru/1/indexes/*/queries/"#"https://mnrwefss2q-dsn.algolia.net/1/indexes/*/queries"
#
# params = {
#     "x-algolia-agent": "Algolia for JavaScript (3.35.1); Browser; react (16.13.1); react-instantsearch (6.6.0); JS Helper (3.1.2)",
#     "x-algolia-application-id": "MNRWEFSS2Q",
#     "x-algolia-api-key": "a3a4de2e05d9e9b463911705fb6323ad"
# }
#
# post_json = {
#     "requests":[
#         {
#             "indexName": "Listing_production",
#             "params": urlencode({
#                 "highlightPreTag": "<ais-highlight-0000000000>",
#                 "highlightPostTag": "</ais-highlight-0000000000>",
#                 "maxValuesPerFacet": "100",
#                 "hitsPerPage": "40",
#                 "filters": "",
#                 "page": "4",
#                 "query": "",
#                 "facets": "[\"designers.name_of_product\",\"category_path\",\"category_size\",\"price_i\",\"condition\",\"location\",\"badges\",\"strata\"]",
#                 "tagFilters": "",
#                 "facetFilters": "[[\"category_path:footwear.hitop_sneakers\"],[\"designers.name_of_product:Jordan Brand\"]]",
#                 "numericFilters": "[\"price_i>=0\",\"price_i<=99999\"]"
#             })
#         }
#     ]
# }
#
# response = requests.post(url, params=params, json=post_json)
# response.raise_for_status()
#
# results = response.json()["results"]
# items = results[0]["hits"]
#
# for item in items:
#     print(f"{item['title']} - price: ${item['price']}")
#     print(f"Image URL: \"{item['cover_photo']['url']}\"\n")
# from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
#
#
# def get_urls(driver):
#     urls = []
#
#     for link in driver.find_elements_by_css_selector('figure.media-thumb.desktop link[itemprop=contentUrl]'):
#         url_gif = link.get_attribute('content')
#         gif_id = url_gif.split('/')[-1]
#         url_download = URL_DOWNLOAD_TEMPLATE + gif_id
#         urls.append(url_download)
#
#     return urls
#
#
# URL_DOWNLOAD_TEMPLATE = 'https://megamarket.ru/catalog/?q=картошка'#'https://i.gifer.com/embedded/download/'
#
#
# options = Options()
# options.add_argument('--headless')
# print("1")
# driver = webdriver.Firefox(options=options)
# print("1")
# driver.get('https://megamarket.ru/catalog/?q=картошка')#'https://gifer.com/ru/gifs/loading')
# print("1")
# driver.implicitly_wait(20)
# print("1")
# urls = get_urls(driver)
# print("1")
# print(f'{len(urls)}: {urls}')
# # 4: ['https://i.gifer.com/embedded/download/g0R5.gif', 'https://i.gifer.com/embedded/download/VAyR.gif', 'https://i.gifer.com/embedded/download/ZKZx.gif', 'https://i.gifer.com/embedded/download/ZZ5H.gif']
# print("1")
# # Small scroll down
# driver.execute_script(f'window.scrollTo(0, 200);')
# print("1")
# urls = get_urls(driver)
# print(f'{len(urls)}: {urls}')
# # 8: ['https://i.gifer.com/embedded/download/g0R5.gif', 'https://i.gifer.com/embedded/download/VAyR.gif', 'https://i.gifer.com/embedded/download/ZKZx.gif', 'https://i.gifer.com/embedded/download/ZZ5H.gif', 'https://i.gifer.com/embedded/download/g0R9.gif', 'https://i.gifer.com/embedded/download/ZWdx.gif', 'https://i.gifer.com/embedded/download/7pld.gif', 'https://i.gifer.com/embedded/download/AqCa.gif']
# print("1")
# driver.quit()
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.common.exceptions import NoSuchElementException
# import chromedriver_binary
# import urllib
# import time
#
# print('start...')
#
# site = "https://www.cian.ru/sale/flat/222059642/"
#
# chrome_options = Options()
# chrome_options.add_argument("--headless")
#
# driver = webdriver.Chrome(options=chrome_options)
# #driver = webdriver.Chrome()
# driver.get(site)
#
# i = 0
#
# while True:
#     try:
#         url = driver.find_element_by_xpath("//div[contains(@class, 'fotorama__active')]/img").get_attribute('src')
#     except NoSuchElementException:
#         break
#
#     i += 1
#     print(i, url)
#
#     driver.find_element_by_xpath("//div[@class='fotorama__arr fotorama__arr--next']").click()
#
#     name_of_product = url.split('/')[-1]
#     urllib.request.urlretrieve(url, name_of_product)
#
#     time.sleep(2)
#
# print('done.')
# from selenium import webdriver
#
# options = webdriver.ChromeOptions()
# options.add_argument('--ignore-certificate-errors')
# options.add_argument("--test-type")
# options.binary_location = "/usr/bin/chromium"
# print("1")
# driver = webdriver.Chrome(options=options)
# print("1")
# driver.get('https://imgur.com/')
# print("1")
# images = driver.find_elements('img')
# for image in images:
#     print(image.get_attribute('src'))
#
# driver.close()

# from selenium import webdriver # Драйвера питона для работы с браузером
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import time
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
#
#
# driver = webdriver.Chrome(ChromeDriverManager().install())
# #chrome_options = Options()
#
# #chrome_options.add_argument("--headless")  # Работа с хромом в невидимом режиме
#
#
# link = 'https://megamarket.ru/catalog/?q=картошка'
#
# driver.get(link) # Ссылка алиэкспреcc
# print(1)
# images = driver.find_elements_by_tag_name('img') # Selenium поиск элемента
# print(1)
# for image in images:
#     print(image.get_attribute('src'))
#
#
#
#
# driver.close()

#PREVIOUS WAS WORKING

# import re
# import json
# from typing import List
#
# import requests
#
#
# def get_images(url: str) -> List[str]:
#     rs = requests.get(url)
#
#     info = re.search('window.__info = (.+?);', rs.text)
#     print(info)
#     if not info:
#         print('[#] Not found window.__info!')
#         return []
#
#     pages = re.search('window.__pg = (.+?);', rs.text)
#     if not pages:
#         print('[#] Not found window.__pg!')
#         return []
#
#     info = json.loads(info.group(1))
#     pages = json.loads(pages.group(1))
#
#     url_chapter = info['img']['url']
#     url_base = info['servers']['main'] + url_chapter
#
#     return [url_base + p['u'] for p in pages]
#
#
# if __name__ == '__main__':
#     url = 'https://megamarket.ru/catalog/?q=картошка'
#     items = get_images(url)
#
#     print(f'Images ({len(items)}):')
#     for i, url in enumerate(items, 1):
#         print(f'    {i}. {url}')


from requests_html import HTMLSession
import requests_html
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
import os
def is_valid(url):
    """
    Проверяем, является ли url действительным URL
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)
def get_all_images(url):
    """
    Возвращает все URL‑адреса изображений по одному `url`
    """
    # инициализировать сеанс
    session = HTMLSession()
    # делаем HTTP‑запрос и получаем ответ
    response: requests_html.HTMLResponse = session.get(url=url, timeout=100)
    #print(session.get(url=url).text)
    # выполнить Javascript с таймаутом 20 секунд
    response.html.render(timeout=200)

    #response = session.request(method='get', url=url, timeout=20)#
    #print(response.content)
    # создаем парсер soup
    soup = bs(response.html.html, "html.parser")
    #print(soup)
    urls = []
    #print(soup.find_all("img"))
    for img in tqdm(soup.find_all("img"), "Извлечено изображение"):
        img_url = img.attrs.get("src") or img.attrs.get("data-src") or img.attrs.get("data-original")
        print(img_url)
        if not img_url:
            # если img не содержит атрибута src, просто пропустим
            continue
        # сделаем URL абсолютным, присоединив имя домена к только что извлеченному URL
        img_url = urljoin(url, img_url)
        # удалим URL‑адреса типа '/hsts-pixel.gif?c=3.2.5'
        try:
            pos = img_url.index("?")
            img_url = img_url[:pos]
        except ValueError:
            pass
        # наконец, если URL действителен
        if is_valid(img_url):
            urls.append(img_url)
    # закрыть сеанс, чтобы завершить процесс браузера
    session.close()
    return urls
def download(url, pathname):
    """
    Загружает файл по URL‑адресу и помещает его в папку `pathname`
    """
    # если папка не существует, создадим папку с именем dir
    if not os.path.isdir(pathname):
        os.makedirs(pathname)
    # загружаем тело ответа по частям, а не сразу
    response = requests.get(url, stream=True)
    print(response)
    # получить общий размер файла
    # file_size = int(response.headers.get("Content-Length", 0))
    # # получаем имя файла
    # filename = os.path.join(pathname, url.split("/")[-1])
    # # индикатор выполнения, изменяем единицы измерения на байты вместо итераций (по умолчанию tqdm)
    # progress = tqdm(response.iter_content(1024), f"Downloading {filename}", total=file_size, unit="B", unit_scale=True, unit_divisor=1024)
    # with open(filename, "wb") as f:
    #     for data in progress.iterable:
    #         # записываем прочитанные данные в файл
    #         f.write(data)
    #         # обновим индикатор выполнения вручную
    #         progress.update(len(data))
def main(url, path):
    # получить все изображения
    imgs = get_all_images(url)
    print(imgs)
    for img in imgs:
        # скачать для каждого img
        print(img)
        download(img, path)

url = 'https://megamarket.ru/catalog/details/kartofel-ekonom-100028918880/#?related_search=картошка'
path = 'D:/'
print("OK")
if not path:
    print("BAD")
    # если путь не указан, в качестве имени папки используйте доменное имя rl
    path = urlparse(url).netloc

main(url, path)
