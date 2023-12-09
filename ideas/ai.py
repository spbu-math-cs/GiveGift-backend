import asyncio
import runpy
from typing import List, Optional

import g4f


def generate_link(title: str, min_budget: int, max_budget: int) -> Optional[str]:
    return f"https://www.wildberries.ru/catalog/0/search.aspx?page=1&sort=popular&search={title}&priceU={min_budget}00%3B{max_budget}00"


async def ask_gpt_or_none(num_of_ideas: int, preferences: List[str]):
    """if num_of_ideas <= 0 or num_of_ideas > 10:
        raise RuntimeError("num_of_ideas not in 1..10 is not supported")"""
    try:
        result: str = ""
        response: str = (await asyncio.gather(
            g4f.ChatCompletion.create_async(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system",
                     "content": "Ты ассистент, который подбирает подарки по предпочтениям, без лишних разговоров и описаний."},
                    {"role": "assistant", "content": f"Друг любит {', '.join(preferences)}."},
                    {"role": "assistant", "content": f"Формат вывода: одним словом, через запятую'."},
                    {"role": "user",
                     "content": f"Выдай {num_of_ideas} уникальных идей подарка для друга без описания."},
                ]
            )
        ))[0]
        for message in response:
            result += str(message)
        return result.replace('.', '').split(', ')
    except Exception as e:
        print(e)
        runpy.run_module("g4f")
        return None


# Будем запускать гонкой: если один из запросов выдал быстрее чем остальные, остальные отменяются
# Понимаю, что wait якобы устарел, но в gather'е нет такого флага, как FIRST_COMPLETED. Когда добавят, тогда и поговорим
async def generate_ideas_or_none(tags: List[str], titles: List[str], lock: asyncio.Lock):
    num_of_threads = 1
    finished, unfinished = await asyncio.wait(
        [ask_gpt_or_none(10, tags) for _ in range(num_of_threads)],
        return_when="FIRST_COMPLETED"
    )
    await lock.acquire()
    for idea in set(finished.pop().result()):
        titles.append(idea.capitalize())
    lock.release()
