from abc import ABC, abstractmethod

from application.dto import Post, Title


class IPostRepository(ABC):
    @abstractmethod
    def get_all_titles(self) -> list[Title]:
        pass

    @abstractmethod
    def get_post(self, id: int) -> Post:
        pass
