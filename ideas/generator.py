import asyncio

from ideas.ai import generate_ideas_or_none, generate_link
from ideas.parser import get_image_link_or_none


def generate_ideas(tags: list, num_of_ideas: int, price_range: list):
    titles = []

    # todo: вскоре вообще пользователю запретим указывать, сколько идей он хочет
    """if num_of_ideas > 10 or num_of_ideas <= 0:
        raise RuntimeError("Unsupported. num_of_ideas not in 1..10")
"""

    ioloop = asyncio.new_event_loop()
    asyncio.set_event_loop(ioloop)
    lock = asyncio.Lock()
    try:
        asyncio.run(generate_ideas_or_none(tags=tags, number_of_ideas=num_of_ideas, titles=titles, lock=lock))
    except Exception:
        pass
    # TODO: убрать описание
    return list(filter(lambda idea: idea["img_link"] is not None,
                       [
                           {"title": title,
                            "description": "Обработка изображений поддерживается",
                            "img_link": get_image_link_or_none(product_name=title, min_budget=price_range[0],
                                                               max_budget=price_range[1]),
                            "market_link": generate_link(title=title, min_budget=price_range[0],
                                                         max_budget=price_range[1]),
                            } for title in titles
                       ]))
