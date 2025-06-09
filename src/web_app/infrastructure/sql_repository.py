from sqlalchemy.ext.asyncio.engine import AsyncConnection
from sqlalchemy import select, update, insert, delete

from application.interface.post_repository import IPostRepository
from application.dto import Post

from shared_module.db_utils import decorate_all_methods, connect
from shared_module.models import PostModel


@decorate_all_methods(connect)
class SQLPostRepository(IPostRepository):
    async def create(self, connect: AsyncConnection, post: Post) -> int:
        result = await connect.execute(insert(PostModel).values(title=post.title, 
                                                                content=post.content).returning(PostModel.id))
        await connect.commit()
        return result.scalar_one()


    async def update(self, connect: AsyncConnection, id: int, post: Post) -> None:
        await connect.execute(update(PostModel).where(PostModel.id == id).values(title=post.title, 
                                                                                      content=post.content))
        await connect.commit()


    async def delete(self, connect: AsyncConnection, id: int) -> None:
        await connect.execute(delete(PostModel).where(PostModel.id == id))
        await connect.commit()


    async def existe(self, connect: AsyncConnection, id: int) -> bool:
        try:
            result = await connect.execute(select(PostModel).where(PostModel.id == id))
            return result.scalar() is not None
        except:
            return False


    async def get(self, connect: AsyncConnection, id: int) -> Post:
        result = await connect.execute(select(PostModel).where(PostModel.id == id))
        title, content, _, _ = result.fetchone()
        return Post(title=title,
                    content=content)
