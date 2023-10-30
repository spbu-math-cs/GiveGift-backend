import openai
from flask import Flask, request, jsonify

openai.api_key = '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'


def generate_present(context, role, max_budget):
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[
            {"role": "system", "content": "Ты полезный ассистент, идеально подбирает подарки по предпочтения."},
            {"role": "assistant", "content": f"Учти, {role} любит {context}."},
            {"role": "user", "content": f"Учитывая эти предпочтения,"
                f" выдай 5 идей подарка в двух-трех словах для {role} стоимостью до {max_budget} рублей,"
                f" который можно купить в любом интернет-магазине"}
        ])
        recommendation = completion.choices[0].message.content
        return recommendation.split('\n')

def link_to_market(str):
    request=str.split()
    request.pop(0)
    link = "https://megamarket.ru/catalog/?q="
    for q in request:
        link+="%20"+q
    if link[-1]=='.':
        link[:-1]
    return link


