import asyncio

from ideas.ai import generate_title_or_none, generate_link
from ideas.parser import get_image_link_or_none


class IdeaGenerator:
    def __init__(self):
        self.__previous_ideas: list = None

    async def generate_one_idea(self, tags: list, price_interval: list, lock: asyncio.Lock):
        title = generate_title_or_none(tags=tags, min_budget=price_interval[0], max_budget=price_interval[1])
        if title is None:
            self.__previous_ideas = None
            return None
        link = generate_link(title=title, min_budget=price_interval[0], max_budget=price_interval[1])
        image_link = get_image_link_or_none(product_name=title, min_budget=price_interval[0],
                                            max_budget=price_interval[1])
        if link is None or image_link is None:
            self.__previous_ideas = None
            return None
        await lock.acquire()
        self.__previous_ideas.append(
            {
                "title": title,
                "description": "Обработка изображений поддерживается",
                "img_link": image_link,
                "market_link": link,
            }
        )
        lock.release()

    def generate_ideas(self, tags: list, num_of_ideas: int, price_interval: list):
        self.__previous_ideas = []
        if num_of_ideas > 5 or num_of_ideas <= 0:
            raise RuntimeError("Unsupported")
        ioloop = asyncio.new_event_loop()
        asyncio.set_event_loop(ioloop)
        lock = asyncio.Lock()
        tasks = [
            ioloop.create_task(self.generate_one_idea(tags=tags, price_interval=price_interval, lock=lock))
            for i in range(num_of_ideas)
        ]
        try:
            ioloop.run_until_complete(asyncio.wait(tasks))
        except IndexError:
            pass
        finally:
            ioloop.close()
        if self.__previous_ideas is None:
            self.__previous_ideas = []
        return self.__previous_ideas

    def get_previous_ideas(self):
        if self.__previous_ideas is None:
            raise Exception("Use has_previous_ideas()!")
        return self.__previous_ideas

    def has_previous_ideas(self):
        return self.__previous_ideas is not None
