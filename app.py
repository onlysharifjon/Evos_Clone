from aiogram import types, Bot, Dispatcher, executor
import logging
from state.states import UserStates, ProductStates
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.types import Contact

from database import *
from keyboards.default import *
from keyboards.default import menu_2
from database import cursor

logging.basicConfig(level=logging.INFO)
API_TOKEN = "6836477622:AAG7yRCuh9OvfcydpbgOy7urLxJoPBX9sW8"
bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands="start")
async def start(message: types.Message):
    user_id = message.from_user.id
    result = await check_user(user_id)

    if result is True:
        await message.answer('Assalomu Aleykum Evos Dastavka Botiga Xush kelibsiz', reply_markup=main_menu)

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


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def text(message: types.Message):
    if message.text == "🍴Menyu":
        await message.answer("Tanlang:", reply_markup=menu_2)
    elif message.text == "Setlar":
        get = cursor.execute('SELECT name FROM products').fetchall()
        print(get)

        get_button = ReplyKeyboardMarkup(resize_keyboard=True)

        buttons_per_row = 2
        current_row = []
        for i, product in enumerate(get, start=1):
            current_row.append(KeyboardButton(text=f"{product[0]}"))
            if i % buttons_per_row == 0 or i == len(get):
                get_button.row(*current_row)
                current_row = []
        await message.answer('setlar', reply_markup=get_button)
        await ProductStates.product.set()


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=ProductStates.product)
async def text(message: types.Message, state: FSMContext):
    global i

    print(True)

    get = cursor.execute('SELECT * FROM products WHERE name=?', (message.text,)).fetchall()


    for i in get:
        print(i)


    image = i[0]
    name = i[1]
    price = i[2]
    category = i[3]


    await bot.send_photo(message.chat.id, open(image, 'rb'),
                         caption=f"<b>{name}</b> \n\n💸narxi - <i>{price}so'm</i> \n\n\n{category} Bo'limidan")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
