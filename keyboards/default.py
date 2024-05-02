from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Send number📱", request_contact=True),
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
    )