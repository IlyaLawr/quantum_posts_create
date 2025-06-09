from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from application.use_case.show_all_titles import ShowAllTitles

from presentation.keyboards.inline import get_paginated_posts_keyboard


def register_start_command_handler(router: Router) -> None:
    @router.message(Command('start'))
    async def start_command_handler(message: Message) -> None:
        await message.answer('*Hello team lead from Quantum.*', parse_mode='Markdown')


def register_posts_command_handler(use_case: ShowAllTitles, router: Router) -> None:
    @router.message(Command('posts'))
    async def posts_command_handler(message: Message) -> None:
        post_titles = await use_case.execute()

        keyboard = get_paginated_posts_keyboard(post_titles, page=0)

        response_text = '*Выберите пост 📃:*' if keyboard else '*На данный момент постов нет.*'

        await message.answer(response_text, reply_markup=keyboard, parse_mode='Markdown')
