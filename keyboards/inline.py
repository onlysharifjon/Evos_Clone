from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

product_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
        InlineKeyboardButton(text="-", callback_data="minus"),
        InlineKeyboardButton(text="0", callback_data="default"),
        InlineKeyboardButton(text="+", callback_data="plus"),
        ],
        [
        InlineKeyboardButton(text="Savatchaga qo'shish📥", callback_data="karzinka"),
        ]
    ],
)


ball_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="1", callback_data="1"),
        ],
        [
            InlineKeyboardButton(text="2", callback_data="2"),
        ],
        [
            InlineKeyboardButton(text="3", callback_data="3"),
        ],
        [
            InlineKeyboardButton(text="4", callback_data="4"),
        ],
        [
            InlineKeyboardButton(text="5", callback_data="5"),
        ],
    ],
)