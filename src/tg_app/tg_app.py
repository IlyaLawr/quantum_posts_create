from asyncio import run
from aiogram import Bot, Dispatcher, Router

from init_path import cleanup_path

from infrastructure.sql_repository import SQLPostRepository

from application.use_case.show_all_titles import ShowAllTitles
from application.use_case.show_post import ShowPost

from presentation.handlers.commands import (register_start_command_handler,
                                            register_posts_command_handler)

from presentation.handlers.callbacks import (register_post_callback_handler,
                                             register_pagination_callback_handler,
                                             register_do_nothing_callback)

from shared_module.settings import settings


async def main():
    repository = SQLPostRepository()

    show_all_titles = ShowAllTitles(repo=repository)
    show_post = ShowPost(repo=repository)

    command_router = Router()
    callback_router = Router()

    register_start_command_handler(router=command_router)
    register_posts_command_handler(use_case=show_all_titles,
                                   router=command_router)
    
    register_post_callback_handler(use_case=show_post,
                                   router=callback_router)
    register_pagination_callback_handler(use_case=show_all_titles,
                                         router=callback_router)
    register_do_nothing_callback(router=callback_router)

    bot = Bot(token=settings.bot_token)

    dp = Dispatcher()

    dp.include_router(command_router)
    dp.include_router(callback_router)


    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    from shared_module.db_utils import create_table
    create_table()

try:
    run(main())
finally:
    cleanup_path()
