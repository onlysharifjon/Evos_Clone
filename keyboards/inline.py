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