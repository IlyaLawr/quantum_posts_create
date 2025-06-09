from application.interface.post_repository import IPostRepository
from application.dto import Title


class ShowAllTitles:
    def __init__(self, repo: IPostRepository) -> None:
        self.repo = repo


    async def execute(self) -> list[Title]:
        titles = await self.repo.get_all_titles()
        return titles
