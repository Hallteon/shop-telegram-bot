from aiogram.dispatcher.filters.state import StatesGroup, State


class Add_Good_State(StatesGroup):
    get_name = State()
    get_author = State()
    get_price = State()
    get_image = State()