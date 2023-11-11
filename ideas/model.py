from ideas.ai import generate_title_or_none, generate_link
from ideas.parser import get_image_link_or_none


class IdeaGenerator:
    def __init__(self):
        # noinspection PyTypeChecker
        self.__previous_ideas: list = None

    def generate_ideas(self, tags: list, num_of_ideas: int, price_interval: list):
        self.__previous_ideas = []
        if num_of_ideas > 1 or num_of_ideas < 0:
            raise RuntimeError("Unsupported")
        for i in range(num_of_ideas):
            title = generate_title_or_none(tags=tags, min_budget=price_interval[0], max_budget=price_interval[1])
            if title is None:
                self.__previous_ideas = None
                return None
            link = generate_link(title=title, min_budget=price_interval[0], max_budget=price_interval[1])
            image_link = get_image_link_or_none(product_name=title, min_budget=price_interval[0], max_budget=price_interval[1])
            if link is None or image_link is None:
                self.__previous_ideas = None
                return None
            self.__previous_ideas.append(
                {
                    "title": title,
                    "description": "Обработка изображений поддерживается",
                    "img_link": image_link,
                    "market_link": link,
                }
            )
        return self.__previous_ideas

    def get_previous_ideas(self):
        if self.__previous_ideas is None:
            raise Exception("Use has_previous_ideas()!")
        return self.__previous_ideas

    def has_previous_ideas(self):
        return self.__previous_ideas is not None
