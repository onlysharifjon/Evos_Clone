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
from database import cursor
from keyboards.inline import *

logging.basicConfig(level=logging.INFO)
API_TOKEN = "6809313060:AAGNE1_ahY5Dt9DMDhU34SgwznJZoH7qc6c"
bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())
OSHXONA = 259083453
kurer = 5172746353
    
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


@dp.message_handler(text="Orqaga🔙", state='*')
async def orqaga(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Siz asosiy menudasiz  :", reply_markup=main_menu)


@dp.message_handler(text="Setlar")
async def set(message: types.Message):
    get = cursor.execute('SELECT name FROM products').fetchall()

    get_button = ReplyKeyboardMarkup(

    )

    buttons_per_row = 2
    current_row = []
    for i, product in enumerate(get, start=1):
        current_row.append(KeyboardButton(text=f"{product[0]}"))
        if i % buttons_per_row == 0 or i == len(get):
            get_button.row(*current_row)
            current_row = []
    get_button.add(KeyboardButton(text="Orqaga🔙"))
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
async def inline_button(call: CallbackQuery, state: FSMContext, ):
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
        await call.message.delete()


@dp.message_handler(text="Atkaz❌")
async def atkaz_products(message: types.Message):
    cursor.execute("DELETE FROM savat WHERE user_id=?", (message.chat.id,))
    await message.answer("Atkaz qilindi", reply_markup=main_menu)


@dp.message_handler(text="Qabul qilaman✅")
async def qilindi_products(message: types.Message):
    product = cursor.execute("SELECT * FROM savat WHERE user_id=? ", (message.from_user.id,)).fetchall()
    all_text = ''
    for i in product:
        all_text += f"🍟{i[2]}\n🔢Soni: {i[3]}\n\n"
    inlne_sender = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Tayyor", callback_data=f"{message.from_user.id}"),
            ]
        ]
    )
    await bot.send_message(OSHXONA, all_text, reply_markup=inlne_sender)


@dp.callback_query_handler()
async def cook(call: types.CallbackQuery):
    global d
    if call.message.chat.id == OSHXONA:
        print("Oshxona ishladi")
        product = cursor.execute("SELECT * FROM savat WHERE user_id=?", (call.message.chat.id,)).fetchall()
        all_text = ''
        button_data = []  # Store the necessary data for each button

        for i in product:
            print(i)
            all_text += f"🍟{i[2]}\n🔢Soni: {i[3]}\n\n"
            await buyurtmalar_tarixi(int(call.data), i[2], i[3])
            connect.commit()
            button_data.append((i[1], i[2]))  # Store data for callback

        cursor.execute('DELETE FROM savat WHERE user_id=?', (str(call.data),))
        connect.commit()

        await bot.send_message(call.data,
                               text=f'{all_text}\nBuyurtmangizni yetkazish uchun kuryer yo`lga chiqdi')
        await call.message.delete()

        kurer_inline = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Yetkazib berdim", callback_data=f"{call.data}")  # Use stored data
                ]
            ]
        )
        await bot.send_message(kurer, f'{all_text} - Sizga buyurtma berildi🚚\n\n Yolga otlaning\n',
                               reply_markup=kurer_inline)

    elif call.message.chat.id == kurer:
        print("Kuryer ishladi")
        product = cursor.execute("SELECT * FROM savat WHERE user_id=?", (call.message.chat.id,)).fetchall()
        for d in product:
            print(d)
        connect.commit()
        await bot.send_message(chat_id=int(OSHXONA), text="<b>🍕Buyurtmangiz Yetkazildi !</b>⚜️\n\n<i>Yetkazib berish hizmatimizni baholang🪙</i>", reply_markup=ball_inline)
        await bot.send_message(kurer, "<i>Tavar Muvofaqiyatli qabul qilib olindi🍕</i>")
        await call.message.delete()
        await ballStates.ball.set()


@dp.callback_query_handler(state=ballStates.ball)
async def ball_for_delivery(call: types.CallbackQuery, state: FSMContext):
    if call.data == "1":
        await call.message.delete()
        await bot.send_photo(kurer , open("uploads/evos/5.png", 'rb'),
                             caption=f"Foydalanvuchi sizni baholadi 🤬",
                             )
        await state.finish()


    elif call.data == "2":
        await call.message.delete()
        await bot.send_photo(kurer , open("uploads/evos/4.png", 'rb'),
                             caption=f"Foydalanvuchi sizni baholadi 😭",
                             )
        await state.finish()


    elif call.data == "3":
        await call.message.delete()
        await bot.send_photo(kurer , open("uploads/evos/3.png", 'rb'),
                             caption=f"Foydalanvuchi sizni baholadi 😮‍💨",)
        await state.finish()


    elif call.data == "4":
        await call.message.delete()
        await bot.send_photo(kurer , open("uploads/evos/2.png", 'rb'),
                             caption=f"Foydalanvuchi sizni baholadi 👍🏻",)
        await state.finish()


    elif call.data == "5":
        await call.message.delete()
        await bot.send_photo(kurer , open("uploads/evos/1.png", 'rb'),
                             caption=f"Foydalanvuchi sizni baholadi 😋🍕",)
        await state.finish()
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
