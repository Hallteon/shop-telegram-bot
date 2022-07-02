import logging
from aiogram import Dispatcher
from data.config import ADMINS


async def on_startup_notify(dp: Dispatcher):
    bot_name = await dp.bot.get_me()

    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, f"<b>Бот \"{bot_name.first_name}\" запущен!</b>")

        except Exception as err:
            logging.exception(err)
