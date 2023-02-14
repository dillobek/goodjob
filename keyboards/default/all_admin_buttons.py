from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


first = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📤 Post yuborish")
        ]
    ],
    resize_keyboard=True
)

tasdiq = ReplyKeyboardMarkup (
    keyboard=[
        [
            KeyboardButton(text="✅ ha"),
            KeyboardButton(text="❌ yo'q")
        ]
    ],
    resize_keyboard=True,

)

edit_menu = ReplyKeyboardMarkup (
    keyboard=[
        [
            KeyboardButton(text="🎓 Kurslar bo'limi"),
            KeyboardButton(text="📚 Kitoblar bo'limi")
        ],
        [
            KeyboardButton(text="🔙 Ortga")
        ]
    ],
    resize_keyboard=True
)


