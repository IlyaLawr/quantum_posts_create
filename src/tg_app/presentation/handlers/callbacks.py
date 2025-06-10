from aiogram import Router, F
from aiogram.types import CallbackQuery

from application.use_case.show_all_titles import ShowAllTitles
from application.use_case.show_post import ShowPost

from presentation.keyboards.callback_factories import (PostCallbackFactory, 
                                                       NavigationCallbackFactory)
from presentation.keyboards.inline import (get_post_detail_keyboard, 
                                           get_paginated_posts_keyboard)

router = Router()


def register_post_callback_handler(use_case: ShowPost, router: Router) -> None:
    @router.callback_query(PostCallbackFactory.filter())
    async def select_post_handler(callback: CallbackQuery,
                                  callback_data: PostCallbackFactory):
 
        post = await use_case.execute(callback_data.id)
        if not post:
            await callback.answer('Пост не найден.', show_alert=True)
            return

        keyboard = get_post_detail_keyboard(current_page=callback_data.page)

        response_text = f'{post.content}\n\n*Дата создания:* {post.date}'
    
        await callback.message.edit_text(response_text, reply_markup=keyboard, parse_mode='Markdown')
        await callback.answer()


def register_pagination_callback_handler(use_case: ShowAllTitles, router: Router) -> None:
    @router.callback_query(NavigationCallbackFactory.filter(F.action == 'paginate'))
    async def pagination_handler(callback: CallbackQuery, 
                                 callback_data: NavigationCallbackFactory):

        post_titles = await use_case.execute()
        keyboard = get_paginated_posts_keyboard(post_titles, page=callback_data.page)

        response_text = '*Выберите пост 📃:*' if keyboard else '*На данный момент постов нет.*'

        await callback.message.edit_text(response_text, reply_markup=keyboard, parse_mode='Markdown')
        await callback.answer()


def register_do_nothing_callback(router: Router) -> None:
    @router.callback_query(F.data == 'do_nothing')
    async def do_nothing_handler(callback: CallbackQuery):
        await callback.answer()
