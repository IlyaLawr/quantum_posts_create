from application.dto import Post
from application.interface.post_repository import IPostRepository


class UpdatePost:
    def __init__(self, repo: IPostRepository):
        self.repo = repo


    async def execute(self, id: int, title: str, content: str) -> bool:
        if await self.repo.existe(id):
            post = await self.repo.get(id)
            new_post = self._forming_updated_post(title=title,
                                                  content=content,
                                                  post=post)

            await self.repo.update(id=id, post=new_post)
            return True
        else:
            return False


    def _forming_updated_post(self, title: str, content: str, post: Post) -> Post:
        modified_post = Post(title='', content='')

        if title:
            if title != post.title:
                modified_post.title = title
            else:
                modified_post.title = post.title
        else:
            modified_post.title = post.title


        if content:
            if content != post.content:
                modified_post.content = content
            else:
                modified_post.content = post.content
        else:
            modified_post.content = post.content

        return modified_post
