from ai import title_with_link


class IdeaGenerator:
    def __init__(self):
        # noinspection PyTypeChecker
        self.__previous_ideas: list = None

    def generate_ideas(self, tags: list, num_of_ideas: int, price_interval: list):
        link_title = title_with_link(str(tags)[1:-1], "друг", price_interval[1], num_of_ideas, price_interval[0])
        if link_title is None:
            self.__previous_ideas = None
        self.__previous_ideas = [
            {
                "title": link_title[0],
                "description": "Обработка изображений не поддерживается",
                "img_link": "https://all-t-shirts.ru/goods_images/1717/1880/ru111223/ru111223II0008e81d0e64a4b4984530b336bbe8be70d.jpg",
                "market_link": link_title[1],
            }
        ]
        return self.__previous_ideas

    def get_previous_ideas(self):
        if self.__previous_ideas is None:
            raise Exception("Use has_previous_ideas()!")
        return self.__previous_ideas

    def has_previous_ideas(self):
        return self.__previous_ideas is not None
