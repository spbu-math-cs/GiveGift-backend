from typing import Optional
import asyncio
import g4f


# noinspection PyBroadException
async def ask_gpt_or_none_async(query: str) -> Optional[str]:
    try:
        result: str = ""
        response = (await asyncio.gather(
            g4f.ChatCompletion.create_async(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": query}],
            )
        ))[0]
        for message in response:
            result += str(message)
        return result
    except Exception as e:
        print(e)
        return None


async def generate_title_or_none_async(tags: list, min_budget: int, max_budget: int, number_of_title: int = 0) -> \
        Optional[str]:
    result: Optional[str] = (await asyncio.gather(ask_gpt_or_none_async(
        f"Сгенерируй одну идею, что подарить человеку, если он любит "
        + str(tags)[
          1: -1] + f", если я готов потратить от {min_budget} до {max_budget} рублей. Ответ выдай одним словом, которое содержит букву {'абвгдеёжзиклмнопрстуфхцчшщъыьэюя'[number_of_title % 33]}"
    )))[0]
    if len(result) > 1000:
        return None
    return result


def generate_link(title: str, min_budget: int, max_budget: int) -> Optional[str]:
    return f"https://www.wildberries.ru/catalog/0/search.aspx?page=1&sort=popular&search={title}&priceU={min_budget}00%3B{max_budget}00"
