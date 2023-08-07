from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
main_menu = [
    [KeyboardButton(text="📅 Узнать график работы"),
    KeyboardButton(text="📆 Мероприятия")],
    [KeyboardButton(text="🗺️ Молодёжный клуб РГО"),
    KeyboardButton(text="🏺 Музей")],
    [KeyboardButton(text="💳 Пушкинская карта"),
    KeyboardButton(text="🎨 Кружки")]
]
main_menu = ReplyKeyboardMarkup(keyboard=main_menu, resize_keyboard=True)
