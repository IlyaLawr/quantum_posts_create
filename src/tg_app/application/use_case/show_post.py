from application.interface.post_repository import IPostRepository
from application.dto import Post


class ShowPost:
    def __init__(self, repo: IPostRepository) -> None:
        self.repo = repo


    async def execute(self, id: int) -> Post:
        post = await self.repo.get_post(id)
        return post
