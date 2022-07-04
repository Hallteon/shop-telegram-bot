import filters, middlewares, handlers
from aiogram import executor
from loader import dp
from utils import notify_admins, set_bot_commands
from utils.db_suff.connect_db import connect
from utils.db_suff.db_functions import create_table


async def on_startup(dispatcher):
    await notify_admins.on_startup_notify(dispatcher)
    await set_bot_commands.set_default_commands(dispatcher)
    await create_table()


async def on_shutdown(dispatcher):
    connect.close()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
