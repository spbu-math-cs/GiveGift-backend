import openai
import requests
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup


url = 'https://megamarket.ru'
response = requests.get(url)
print(response.status_code)
images = []

soup = BeautifulSoup(response.text, features="html.parser")
#print(soup) #
img_tag = soup.find('img')
print(img_tag)
if img_tag:
        # Извлекаем ссылку на фотографию из атрибута src
    photo_url = img_tag['src']
    print("Ссылка на первую фотографию:", photo_url)
else:
    print("Фотографии не найдены на странице.")
#print(images)
