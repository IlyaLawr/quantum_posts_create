from sqlalchemy.ext.asyncio.engine import AsyncConnection
from sqlalchemy import select

from application.interface.post_repository import IPostRepository
from application.dto import Post, Title

from shared_module.db_utils import decorate_all_methods, connect
from shared_module.models import PostModel


@decorate_all_methods(connect)
class SQLPostRepository(IPostRepository):
    async def get_all_titles(self, connect: AsyncConnection) -> list[Title]:
        result = await connect.execute(select(PostModel.id, PostModel.title, ))

        titles = []
        for data in result.all():
            titles.append(Title(post_id=data[0],
                                content=data[1]))

        return titles


    async def get_post(self, connect: AsyncConnection, id: int) -> Post | None:
        result = await connect.execute(select(PostModel.id,
                                              PostModel.title,
                                              PostModel.content,
                                              PostModel.created_at).where(PostModel.id == id))
        data = result.fetchone()
        if data:
            return Post(id=data[0],
                        title=data[1],
                        content=data[2],
                        date=data[3].strftime("%d.%m.%Y %H:%M:%S"))
