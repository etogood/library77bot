from aiogram.types import InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

import db
import text

main_menu = [
    [KeyboardButton(text="📅 Узнать график работы"),
    KeyboardButton(text="📆 Мероприятия")],
    [KeyboardButton(text="🗺️ Молодёжный клуб РГО"),
    KeyboardButton(text="🏺 Музей")],
    [KeyboardButton(text="💳 Пушкинская карта"),
    KeyboardButton(text="🎨 Кружки")]
]
main_menu = ReplyKeyboardMarkup(keyboard=main_menu, resize_keyboard=True)


classes_builder = ReplyKeyboardBuilder()
dic = db.get_classes()
for item in dic:
    classes_builder.button(text = item.name)
classes_builder.button(text = text.menu)
classes_builder.adjust(dic.count() // 5)
classes_menu = classes_builder.as_markup(resize_keyboard=True)


