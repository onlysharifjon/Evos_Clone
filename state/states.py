from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup,State


class UserStates(StatesGroup):
    phone_number = State()
    location = State()


class ProductStates(StatesGroup):
    product = State()
