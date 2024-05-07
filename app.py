from aiogram import types, Bot, Dispatcher, executor
import logging
from state.states import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from aiogram.types import Contact, CallbackQuery

from database import *
from keyboards.default import *
from keyboards.default import menu_2
from database import cursor
from keyboards.inline import *

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


@dp.message_handler(text="🍴Menyu")
async def meni(message: types.Message):
    await message.answer("Tanlang:", reply_markup=menu_2)


@dp.message_handler(text="Orqaga🔙")
async def orqaga(message: types.Message):
    await message.answer("Siz asosiy menudasiz  :", reply_markup=main_menu)

@dp.message_handler(text="Setlar")
async def set(message: types.Message):
    get = cursor.execute('SELECT name FROM products').fetchall()

    get_button = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Orqaga🔙")
            ]
        ]
    )

    buttons_per_row = 2
    current_row = []
    for i, product in enumerate(get, start=1):
        current_row.append(KeyboardButton(text=f"{product[0]}"))
        if i % buttons_per_row == 0 or i == len(get):
            get_button.row(*current_row)
            current_row = []
    await message.answer('setlar', reply_markup=get_button)
    await ProductStates.product.set()


@dp.message_handler(text="Savat")
async def save(message: types.Message):
    savat = cursor.execute("SELECT * FROM savat WHERE user_id=?", (message.from_user.id,)).fetchall()
    nomi = str(savat[0][2])
    txt = ''
    all = 0
    for i in savat:
        price = cursor.execute("SELECT * FROM products WHERE name=?", (i[2],)).fetchall()
        print(price)
        obshi_narxi = i[3] * price[0][2]
        all += obshi_narxi
        txt += f"""
<b>Mahsulot nomi:</b>  <i>{i[2]}</i> 🍟
<b>Mahsulot Soni:</b>   <i>{i[3]} </i>
<b>Mahsulot Narxi:</b>  <i>{price[0][2]} </i>\n
        """
    txt += f"                               <b>Mahsulotlar narxi :</b> <i>{all}so'm💸</i>"

    await message.answer(txt, reply_markup=btn_in_savat)


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=ProductStates.product)
async def text(message: types.Message, state: FSMContext):
    global i
    global name

    await check_count(message.from_user.id)

    get = cursor.execute('SELECT * FROM products WHERE name=?', (message.text,)).fetchall()

    for i in get:
        print("s")

    image = i[0]
    name = i[1]
    price = i[2]
    category = i[3]

    await bot.send_photo(message.chat.id, open(image, 'rb'),
                         caption=f"<b>{name}</b> \n\n💸narxi - <i>{price}so'm</i> \n\n\n{category} Bo'limidan",
                         reply_markup=product_inline)

    # async def update_pluster(message: types.Message):
    #     pass
    # async def update_minuser(message: types.Message):
    #     pass

@dp.callback_query_handler(state=ProductStates.product)
async def inline_button(call: CallbackQuery, state: FSMContext,):
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    if call.data == 'plus':
        cursor.execute('UPDATE counts SET count=count + 1 WHERE user_id=?', (call.message.chat.id,))
        connect.commit()
        soni = cursor.execute('SELECT * FROM counts WHERE user_id=?', (call.message.chat.id,)).fetchall()[0][2]
        product_inline = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="-", callback_data="minus"),
                    InlineKeyboardButton(text=f"{soni}", callback_data="default"),
                    InlineKeyboardButton(text="+", callback_data="plus"),
                ],
                [
                    InlineKeyboardButton(text="Savatchaga qo'shish📥", callback_data="karzinka"),
                ]
            ],
        )
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id, reply_markup=product_inline,
                                            message_id=call.message.message_id)



    elif call.data == 'minus':
        cursor.execute('UPDATE counts SET count=count - 1 WHERE user_id=?', (call.message.chat.id,))
        connect.commit()
        soni = cursor.execute('SELECT * FROM counts WHERE user_id=?', (call.message.chat.id,)).fetchall()[0][2]
        product_inline = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="-", callback_data="minus"),
                    InlineKeyboardButton(text=f"{soni}", callback_data="default"),
                    InlineKeyboardButton(text="+", callback_data="plus"),
                ],
                [
                    InlineKeyboardButton(text="Savatchaga qo'shish📥", callback_data="karzinka"),
                ]
            ],
        )
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id, reply_markup=product_inline,
                                            message_id=call.message.message_id)
    elif call.data == 'karzinka':
        r = cursor.execute("SELECT * FROM counts WHERE user_id=?", (call.message.chat.id,))
        for i in r:
            print(i)
        user_id = i[1]
        count = i[2]

        product = cursor.execute("SELECT * FROM products WHERE name=? ", (name,)).fetchall()
        product_name = product[0][1]
        product_price = product[0][2]
        print(product)

        add_in_savat(user_id, product_name, count)

        await call.answer("buyurtmangiz savatchaga🤵‍♂️ \nTuwdi uni qabul qilib oling✅/❌")



@dp.message_handler(text="Atkaz❌")
async def atkaz_products(message: types.Message):
    cursor.execute("DELETE FROM savat WHERE user_id=?", (message.chat.id,))
    await message.answer("Atkaz qilindi", reply_markup=main_menu)





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
