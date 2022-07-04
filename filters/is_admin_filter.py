from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.config import ADMINS
from loader import bot


class Is_Admin(BoundFilter):

    async def check(self, message: types.Message):
        return str(message.from_user.id) in ADMINS