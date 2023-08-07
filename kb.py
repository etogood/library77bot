from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

import db
import text

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)

main_menu = [
    [KeyboardButton(text = text.schedule_button_text),
    KeyboardButton(text = text.events_button_text)],
    [KeyboardButton(text = text.youth_club_button_text),
    KeyboardButton(text = text.museum_button_text)],
    [KeyboardButton(text = text.pushkin_card_button_text),
    KeyboardButton(text = text.classes_button_text)]
]
main_menu = ReplyKeyboardMarkup(keyboard = main_menu, resize_keyboard = True)

return_menu = ReplyKeyboardMarkup(keyboard = [[KeyboardButton(text = text.main_menu)]], resize_keyboard = True)

classes_builder = ReplyKeyboardBuilder()
dic = db.get_classes()
for item in dic:
    classes_builder.button(text = item.name)
classes_builder.button(text = text.main_menu)
classes_builder.adjust(dic.count() // 5)
classes_menu = classes_builder.as_markup(resize_keyboard=True)


youth_club_menu = InlineKeyboardMarkup(
    inline_keyboard = [[InlineKeyboardButton(text = text.apply_button_text, callback_data = "apply_for_club_membership")]])