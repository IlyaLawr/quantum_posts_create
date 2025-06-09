from fastapi import Depends

from infrastructure.sql_repository import SQLPostRepository

from application.interface.post_repository import IPostRepository

from application.use_case.create_post import CreatePost
from application.use_case.delete_post import DeletePost
from application.use_case.update_post import UpdatePost


def get_post_repository() -> IPostRepository:
    return SQLPostRepository()


def get_create_post_use_case(
        repo: IPostRepository = Depends(get_post_repository)) -> CreatePost:

    return CreatePost(repo=repo)


def get_delete_post_use_case(
        repo: IPostRepository = Depends(get_post_repository)) -> DeletePost:

    return DeletePost(repo=repo)


def get_update_post_use_case(
        repo: IPostRepository = Depends(get_post_repository)) -> UpdatePost:

    return UpdatePost(repo=repo)
