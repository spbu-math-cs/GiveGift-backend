from typing import Optional
import g4f


# noinspection PyBroadException
def ask_gpt_or_none(query: str) -> Optional[str]:
    try:
        result: str = ""
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": query}],
            stream=True,
        )

        for message in response:
            result += str(message)
        return result
    except:
        return None


def generate_title_or_none(tags: list, min_budget: int, max_budget: int) -> Optional[str]:
    result = ask_gpt_or_none(
        f"Сгенерируй одну идею, что подарить человеку, если он любит "
        + str(tags)[1: -1] + f", если я готов потратить от {min_budget} до {max_budget} рублей. Ответ выдай одним словом"
        )
    if len(result) > 1000:
        return None
    return result


def generate_link(title: str, min_budget: int, max_budget: int) -> Optional[str]:
    return f"https://www.wildberries.ru/catalog/0/search.aspx?page=1&sort=popular&search={title}&priceU={min_budget}00%3B{max_budget}00"

