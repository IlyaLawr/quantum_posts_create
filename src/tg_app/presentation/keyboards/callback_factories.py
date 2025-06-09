from aiogram.filters.callback_data import CallbackData


class PostCallbackFactory(CallbackData, prefix="post"):
    id: int
    page: int


class NavigationCallbackFactory(CallbackData, prefix="nav"):
    action: str
    page: int
