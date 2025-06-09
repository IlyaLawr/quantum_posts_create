from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from init_path import app_root, cleanup_path

from presentation.endpoints.posts import router as posts_router
from presentation.endpoints.pages import router as pages_router


try:
    app = FastAPI(
        title='API для управления постами',
        description='Данное API предназначено для создания/удаления и изменения постов.',
        version='1.0.0',
        docs_url='/docs',
        redoc_url='/redoc',
        openapi_url='/openapi.json',
    )


    app.mount('/presentation/static', StaticFiles(directory=f'{app_root}/presentation/static'), name='static')

    app.include_router(pages_router)
    app.include_router(posts_router)
finally:
    cleanup_path()


if __name__ == '__main__':
    from shared_module.db_utils import create_table
    create_table()
