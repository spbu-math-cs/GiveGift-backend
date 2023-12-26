from ideas.ai import generate_ideas_or_none, generate_link
from ideas.parser import get_tuple_title_image


def generate_ideas(tags: list, price_range: list, adult: bool):
    titles = []
    try:
        generate_ideas_or_none(tags=tags, titles=titles)
    except IndexError:
        pass
    try:
        return list(filter(lambda idea: (idea is not None) and (idea["img_link"] is not None),
                           [
                               {"title": get_tuple_title_image(product_name=title, min_budget=price_range[0],
                                                               max_budget=price_range[1], adult=adult)[1],
                                "img_link": get_tuple_title_image(product_name=title, min_budget=price_range[0],
                                                                  max_budget=price_range[1], adult=adult)[0],
                                "market_link": generate_link(title=title, min_budget=price_range[0],
                                                             max_budget=price_range[1]),
                                } for title in titles
                           ]
                           )
                    )
    except IndexError:
        pass
    return []
