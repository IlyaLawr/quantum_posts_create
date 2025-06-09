from math import ceil

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from application.dto import Title
from presentation.keyboards.callback_factories import (PostCallbackFactory, 
                                                       NavigationCallbackFactory)


POSTS_PER_PAGE = 6
POST_BUTTONS_IN_ROW = 2


def get_post_detail_keyboard(current_page: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='⬅️ К списку постов',
                   callback_data=NavigationCallbackFactory(action='paginate', 
                                                           page=current_page).pack())

    return builder.as_markup()


def get_paginated_posts_keyboard(titles: list[Title],
                                 page: int = 0) -> InlineKeyboardMarkup | None:

    if not titles:
        return None

    total_pages = ceil(len(titles) / POSTS_PER_PAGE)
    
    start = page * POSTS_PER_PAGE
    end = start + POSTS_PER_PAGE
    paginated_posts = titles[start:end]

    builder = InlineKeyboardBuilder()

    for title in paginated_posts:
        builder.button(text=title.content,
                       callback_data=PostCallbackFactory(id=title.post_id, page=page))

    builder.adjust(POST_BUTTONS_IN_ROW)

    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text='⬅️ Назад',
                                                callback_data=NavigationCallbackFactory(action='paginate', 
                                                                                        page=page - 1).pack()))
    
    nav_buttons.append(InlineKeyboardButton(text=f'{page + 1} / {total_pages}',
                                            callback_data='do_nothing'))

    if end < len(titles):
        nav_buttons.append(InlineKeyboardButton(text='Вперёд ➡️',
                                                callback_data=NavigationCallbackFactory(action='paginate', 
                                                                                        page=page + 1).pack()))

    if nav_buttons:
        builder.row(*nav_buttons)

    return builder.as_markup()
