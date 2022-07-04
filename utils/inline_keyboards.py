from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils.db_suff.db_functions import get_all_goods

get_good_callback = CallbackData("get_good", "id")
remove_good_callback = CallbackData("remove_good", "id")

admin_panel = InlineKeyboardMarkup()
admin_panel.add(InlineKeyboardButton(text="Добавить товар", callback_data="add_goods"))
admin_panel.add(InlineKeyboardButton(text="Удалить товар", callback_data="remove_goods"))
admin_panel.add(InlineKeyboardButton(text="Выйти", callback_data="exit_from_admin_panel"))

return_to_admin_panel = InlineKeyboardMarkup()
return_to_admin_panel.add(InlineKeyboardButton(text="Вернуться в меню", callback_data="return_to_admin_panel"))

shop_keyboard = InlineKeyboardMarkup()
shop_keyboard.add(InlineKeyboardButton(text="Каталог", callback_data="catalog"))
shop_keyboard.add(InlineKeyboardButton(text="Выйти", callback_data="exit_from_shop"))


async def get_all_goods_keyboard(mode):
    all_goods_keyboard = InlineKeyboardMarkup()
    goods = await get_all_goods()

    for name, author, id in goods:
        callback = None

        if mode == "get":
            callback = get_good_callback.new(id)

        elif mode == "remove":
            callback = remove_good_callback.new(id)

        all_goods_keyboard.add(InlineKeyboardButton(text=f"{name} | {author}", callback_data=callback))

    all_goods_keyboard.add(InlineKeyboardButton(text="Назад", callback_data="back_to_shop_menu"))

    return all_goods_keyboard
