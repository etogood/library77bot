from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
menu = [
    [KeyboardButton(text="📅 Узнать график работы"),
    KeyboardButton(text="📆 Мероприятия")],
    [KeyboardButton(text="🗺️ Молодёжный клуб РГО"),
    KeyboardButton(text="🏺 Музей")],
    [KeyboardButton(text="💳 Пушкинская карта"),
    KeyboardButton(text="🎨 Кружки")]
]
menu = ReplyKeyboardMarkup(keyboard=menu, resize_keyboard=True)
