from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import LabeledPrice, ContentType

from data.config import PAYMENTS_TOKEN
from loader import dp, bot
from states.shop_states import Get_Goods_Page
from utils.db_suff.db_functions import get_good_from_db
from utils.inline_keyboards import shop_keyboard, get_all_goods_keyboard
from utils.payments import post_shipping_option, to_home_shipping_option, pickup_shipping_option


@dp.message_handler(Command("shop"), chat_type=types.ChatType.PRIVATE)
async def send_shop(message: types.Message):
    await message.answer("<b>Вы зашли в меню магазина</b>", reply_markup=shop_keyboard)
    await Get_Goods_Page.first()


@dp.callback_query_handler(text="catalog", state=Get_Goods_Page.page)
async def send_catalog_start(callback: types.CallbackQuery, state: FSMContext):
    keyboards = await get_all_goods_keyboard("get")

    await callback.message.edit_text("<b>Каталог товаров:</b>")
    await callback.message.edit_reply_markup(reply_markup=keyboards[1])

    async with state.proxy() as data:
        data["keyboards"] = keyboards
        data["page"] = 1


@dp.callback_query_handler(text="next_page", state=Get_Goods_Page.page)
async def send_next_page(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data["page"] += 1

    state_data = await state.get_data()
    keyboards = state_data["keyboards"]
    page = state_data["page"]

    await callback.message.edit_text("<b>Каталог товаров:</b>")
    await callback.message.edit_reply_markup(reply_markup=keyboards[page])


@dp.callback_query_handler(text="previous_page", state=Get_Goods_Page.page)
async def send_previous_page(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data["page"] -= 1

    state_data = await state.get_data()
    keyboards = state_data["keyboards"]
    page = state_data["page"]

    await callback.message.edit_text("<b>Каталог товаров:</b>")
    await callback.message.edit_reply_markup(reply_markup=keyboards[page])


@dp.callback_query_handler(text_contains="get_good", state=Get_Goods_Page.page)
async def send_good(callback: types.CallbackQuery, state: FSMContext):
    callback_data = callback.data.strip().split(":")[1:]
    good_id = int(callback_data[0])
    good_information = await get_good_from_db(good_id)
    good_name, good_author, good_price, good_image = good_information
    price = [LabeledPrice(label=f"{good_name} | {good_author}", amount=good_price)]

    await bot.send_invoice(callback.message.chat.id,
                           title=f"Книга \"{good_name}\"",
                           description=f"Автор - {good_author}",
                           provider_token=PAYMENTS_TOKEN,
                           currency="rub",
                           photo_url=good_image,
                           photo_width=220,
                           photo_height=344,
                           photo_size=344,
                           is_flexible=True,
                           prices=price,
                           start_parameter="buy_book",
                           payload="book",
                           need_phone_number=True)

    await callback.message.delete()
    await state.reset_state()


@dp.shipping_query_handler(lambda query: True)
async def shipping_process(shipping_query: types.ShippingQuery):
    if shipping_query.shipping_address.country_code == "RU":
        options = [post_shipping_option]

        if shipping_query.shipping_address.city == "Екатеринбург":
            options.extend([pickup_shipping_option, to_home_shipping_option])

        await bot.answer_shipping_query(shipping_query.id, ok=True,
                                        shipping_options=options)

    else:
        await bot.answer_shipping_query(shipping_query.id, ok=False,
                                        error_message="Извините, но наши товары не "
                                                      "доставляются в вашу страну!")


@dp.pre_checkout_query_handler(lambda query: True)
async def checkout_process(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: types.Message):
    await message.answer("<b>Вы успешно оплатили покупку! В скором времени вы "
                         "получите свой заказ.</b>")


@dp.callback_query_handler(text="back_to_shop_menu", state=Get_Goods_Page.page)
async def back_to_shop_menu(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.reset_state()

    await send_shop(callback.message)


@dp.callback_query_handler(text="exit_from_shop", state=Get_Goods_Page.page)
async def exit_from_shop(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.reset_state()

