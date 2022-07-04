from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from filters import Is_Admin
from loader import dp
from states.shop_states import Add_Good_State
from utils.db_suff.db_functions import add_good_to_db, remove_good_from_db
from utils.inline_keyboards import admin_panel, get_all_goods_keyboard, return_to_admin_panel


@dp.message_handler(Command("admin_panel"), Is_Admin(), chat_type=types.ChatType.PRIVATE)
async def send_admin_panel(message: types.Message):
    await message.answer("<b>Вы вошли в админ-панель для товаров</b>", reply_markup=admin_panel)


@dp.callback_query_handler(text="add_goods")
async def add_good(callback: types.CallbackQuery):
    await callback.message.edit_text("<b>Введите название книги:</b>")

    await Add_Good_State.first()


@dp.message_handler(Is_Admin(), state=Add_Good_State.get_name)
async def get_name(message: types.Message, state: FSMContext):
    await message.answer("<b>Введите автора книги:</b>")

    async with state.proxy() as data:
        data["name"] = message.text

    await Add_Good_State.next()


@dp.message_handler(Is_Admin(), state=Add_Good_State.get_author)
async def get_name(message: types.Message, state: FSMContext):
    await message.answer("<b>Введите цену книги:</b>")

    async with state.proxy() as data:
        data["author"] = message.text

    await Add_Good_State.next()


@dp.message_handler(Is_Admin(), state=Add_Good_State.get_price)
async def get_name(message: types.Message, state: FSMContext):
    await message.answer("<b>Отправьте картинку книги:</b>")

    async with state.proxy() as data:
        data["price"] = int(message.text) * 100

    await Add_Good_State.next()


@dp.message_handler(Is_Admin(), state=Add_Good_State.get_image)
async def get_image(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["image"] = message.text

    state_data = await state.get_data()
    name = state_data["name"]
    author = state_data["author"]
    price = state_data["price"]
    image = state_data["image"]

    await message.answer("<b>Товар успешно добавлен!</b>")

    await add_good_to_db(name, author, price, image)
    await state.reset_state()


@dp.callback_query_handler(Is_Admin(), text="remove_goods")
async def send_remove_goods(callback: types.CallbackQuery):
    await callback.message.edit_text("<b>Нажмите на товар чтобы удалить его:</b>")
    await callback.message.edit_reply_markup(reply_markup=await get_all_goods_keyboard("remove"))


@dp.callback_query_handler(Is_Admin(), text_contains="remove_good")
async def remove_good(callback: types.CallbackQuery):
    callback_data = callback.data.strip().split(":")[1:]
    good_id = callback_data[0]

    await callback.message.edit_text("<b>Товар был успешно удалён!</b>")
    await callback.message.edit_reply_markup(reply_markup=return_to_admin_panel)
    await remove_good_from_db(good_id)


@dp.callback_query_handler(Is_Admin(), text="return_to_admin_panel")
async def return_to_admin_menu(callback: types.CallbackQuery):
    await callback.message.delete()
    await send_admin_panel(callback.message)


@dp.callback_query_handler(Is_Admin(), text="exit_from_admin_panel")
async def exit_from_admin_panel(callback: types.CallbackQuery):
    await callback.message.delete()
