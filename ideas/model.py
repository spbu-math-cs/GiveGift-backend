class IdeaGenerator:
    def __init__(self):
        # noinspection PyTypeChecker
        self.__previous_ideas: list = None

    def generate_ideas(self, tags: list, num_of_ideas: int, price_interval: int):
        self.__previous_ideas = [
            {
                "title": "House",
                "description": "Good house!",
                "img_link": "https://python.org",
                "market_link": "https://python.org",
            }
        ]
        return self.__previous_ideas

    def get_previous_ideas(self):
        if self.__previous_ideas is None:
            raise Exception("Use has_previous_ideas()!")
        return self.__previous_ideas

    def has_previous_ideas(self):
        return self.__previous_ideas is not None
