from pydantic import BaseModel, Field


TITLE: str = Field(..., title='Заголовок', max_length=200, example='Мой первый пост')
CONTENT: str = Field(..., title='Содержимое', example='Текст вашего поста...')


class Post(BaseModel):
    title: str = TITLE
    content: str = CONTENT


class ExistingPost(BaseModel):
    title: str | None = TITLE
    content: str | None = CONTENT
