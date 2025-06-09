from fastapi import APIRouter, Depends, status

from application.use_case.create_post import CreatePost
from application.use_case.update_post import UpdatePost
from application.use_case.delete_post import DeletePost

from presentation.dependencies import get_create_post_use_case
from presentation.dependencies import get_delete_post_use_case
from presentation.dependencies import get_update_post_use_case

from presentation.endpoints.models.posts import Post, ExistingPost
from presentation.endpoints.models.responses import CreateResponse, UpdateResponse, DeleteResponse


router = APIRouter(prefix='/posts', tags=['posts'])


@router.post('/', 
             summary='Создает новый пост.',
             description=f'Создаёт в БД новый пост с полями `title` и `content`. '
                          'Если в БД есть пост с идентичными `title` и `content` то создает второй такой же но с другим `id`.',
             response_description='Возвращает `id` созданного поста и информационное текстовое сообщение с `id` поста.',
             response_model=CreateResponse,
             status_code=status.HTTP_201_CREATED)
async def create(post: Post,
                 use_case: CreatePost = Depends(get_create_post_use_case)) -> CreateResponse:
    id = await use_case.execute(post)

    return CreateResponse(id=id,
                          message=f'Пост с ID {id} создан')


@router.put('/{id}',
            summary='Обновляет существующий пост.',
            description='Обновляет поля `title` и `content` у поста с заданным `id`.',
            response_description='Возвращает булево значение, которое говорит об успешности выполнения запроса и информационное сообщение.',
            response_model=UpdateResponse,
            status_code=status.HTTP_200_OK)
async def update(id: int,
                 exiting_post: ExistingPost,
                 use_case: UpdatePost = Depends(get_update_post_use_case)) -> UpdateResponse:
    success = await use_case.execute(id,
                                     title=exiting_post.title,
                                     content=exiting_post.content)

    if success:
        return UpdateResponse(success=True,
                              message='Пост обновлен')
    else:
        return UpdateResponse(success=False,
                              message='Поста с данным id не существует')


@router.delete('/{id}',
               summary='Удаляет существующий пост.',
               description='Удаляет из БД пост по `id`.',
               response_description='Возвращает булево значение, которое говорит об успешности выполнения запроса и информационное сообщение.',
               response_model=DeleteResponse,
               status_code=status.HTTP_200_OK)
async def delete(id: int,
                 use_case: DeletePost = Depends(get_delete_post_use_case)) -> DeleteResponse:
    success = await use_case.execute(id)

    if success:
        return DeleteResponse(success=True,
                              message='Пост удален')
    else:
        return DeleteResponse(success=False,
                              message='Поста с данным id не существует')
