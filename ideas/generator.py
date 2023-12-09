import asyncio

from ideas.ai import generate_ideas_or_none, generate_link
from ideas.parser import get_image_link_or_none


def generate_ideas(tags: list, price_range: list):
    titles = []
    ioloop = asyncio.new_event_loop()
    asyncio.set_event_loop(ioloop)
    lock = asyncio.Lock()
    try:
        asyncio.run(generate_ideas_or_none(tags=tags, titles=titles, lock=lock))
    except IndexError:
        pass
    return list(filter(lambda idea: idea["img_link"] is not None,
                       [
                           {"title": title,
                            "img_link": get_image_link_or_none(product_name=title, min_budget=price_range[0],
                                                               max_budget=price_range[1]),
                            "market_link": generate_link(title=title, min_budget=price_range[0],
                                                         max_budget=price_range[1]),
                            } for title in titles
                       ]))
