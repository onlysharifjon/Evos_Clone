from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


#Telefon nomer uchun button
keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Send number📱", request_contact=True),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
    )
#Lokatsiya uchun Button

location_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Send location", request_location=True),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# Asosiy Menyu uchun Button

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🍴Menyu"),
        ],
        [
            KeyboardButton(text="📋 Mening buyurtmalarim")
        ],
        [
            KeyboardButton(text="📥 Savat"),
            KeyboardButton(text="📞 Aloqa")
        ],
        [
            KeyboardButton(text="✍️ Xabar Yuborish"),
            KeyboardButton(text="⚙️ Sozlamalar")
        ]
    ]
)


#Keyingi menu uchun button


menu_2 = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Setlar")
        ],
        [
            KeyboardButton(text="Lavash"),
            KeyboardButton(text="Shourma")
        ],
        [
            KeyboardButton(text="Burger"),
            KeyboardButton(text="Hot-dog")
        ],
        [
            KeyboardButton(text="Ichimlikar")
        ],
        [
            KeyboardButton(text="Shirinlikar va Disert")
        ],
        [
            KeyboardButton(text="Garnirlar")
        ],
        [
            KeyboardButton(text="Orqaga🔙")
        ]
    ]
)

