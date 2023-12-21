import datetime
from typing import List, Optional

import g4f


def generate_link(title: str, min_budget: int, max_budget: int) -> Optional[str]:
    # noinspection IncorrectFormatting
    return f"https://www.wildberries.ru/" \
           f"catalog/0/search.aspx?page=1&sort=popular&search={title}&priceU={min_budget}00%3B{max_budget}00"


def ask_gpt_or_none(num_of_ideas: int, preferences: List[str]):
    try:
        response: str = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Use Russian language only"},
                {"role": "user",
                 "content": f"Подбери {num_of_ideas}  подарков человеку,"
                            f" учитывай что он хотел бы получить в качестве подарка что то,"
                            f" что связано с {', '.join(preferences)} и {datetime.datetime.now()}. "
                            f"не пиши описания к подаркам, нужно просто их название"},
            ]
        )
        final_list = []
        for idea in response.split('\n'):
            if idea != '' and any(char.isdigit() for char in idea) and "!" not in idea:
                final_list.append(idea[2:].replace('.', '').strip())
        return final_list
    except Exception as e:
        print(e)
        return None


def generate_ideas_or_none(tags: List[str], titles: List[str]):
    result = ask_gpt_or_none(10, tags)
    if result is not None:
        for idea in result:
            titles.append(idea)
