from abc import ABC, abstractmethod

from application.dto import Post


class IPostRepository(ABC):
    @abstractmethod
    def create(self, post: Post) -> int:
        pass


    @abstractmethod
    def update(self, id: int, post: Post) -> None:
        pass


    @abstractmethod
    def delete(self, id: int) -> None:
        pass


    @abstractmethod
    def existe(self, id: int) -> bool:
        pass


    @abstractmethod
    def get(self, id: int) -> Post:
        pass
