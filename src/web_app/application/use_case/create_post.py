from application.dto import Post
from application.interface.post_repository import IPostRepository


class CreatePost:
    def __init__(self, repo: IPostRepository):
        self.repo = repo


    async def execute(self, post: Post) -> int:
        return await self.repo.create(post)
