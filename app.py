from aiogram import types, Bot, Dispatcher, executor
import logging
from state.states import UserStates
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.types import Contact

from database import *
from keyboards.default import *
from keyboards.default import menu_2

logging.basicConfig(level=logging.INFO)
API_TOKEN = "6836477622:AAG7yRCuh9OvfcydpbgOy7urLxJoPBX9sW8"
bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands="start")
async def start(message: types.Message):
    user_id = message.from_user.id
    result = await check_user(user_id)

    if result is True:
        await message.answer('Assalomu Aleykum Evos Dastavka Botiga Xush kelibsiz',reply_markup=main_menu)

    else:
        await message.answer(
            "Salom Evos Dastavka botiga hush kelibisiz \n Ro'yxatdan otish uchun ttelefon raqamingizni jonating",
            reply_markup=keyboard)
        await  UserStates.phone_number.set()


@dp.message_handler(content_types=types.ContentTypes.CONTACT, state=UserStates.phone_number)
async def contact(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    contact = message.contact
    await add_user(user_id, int(contact.phone_number[5::1]))
    await message.answer(f"{message.from_user.first_name} - Raqamingiz qabul qilindi📞\n ")
    await state.finish()
    await message.answer("<b>Locatsiyangizni jonating</b> 📍", reply_markup=location_kb)
    await UserStates.location.set()


@dp.message_handler(content_types=types.ContentTypes.LOCATION, state=UserStates.location)
async def location(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    longitude = message.location.longitude
    latitude = message.location.latitude
    await update_location(user_id, longitude, latitude)
    await state.finish()
    await message.answer("Siz royxatdan otdingiz!) \n\n ")


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def text(message:types.Message):
    if message.text == "🍴Menyu":
        await message.answer("Tanlang:", reply_markup=menu_2)




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
