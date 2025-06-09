from application.interface.post_repository import IPostRepository


class DeletePost:
    def __init__(self, repo: IPostRepository):
        self.repo = repo

    async def execute(self, id: int) -> bool:
        if await self.repo.existe(id):
            await self.repo.delete(id=id)
            return True
        else:
            return False
