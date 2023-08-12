from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from typing import Optional
from aiogram.filters.callback_data import CallbackData

import db
import text

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class CallbackFactory(CallbackData, prefix="eventfab"):
    action: str
    id: Optional[int]

def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)

main_menu = [
    [InlineKeyboardButton(text = text.schedule_button_text, callback_data = "schedule")],
    [InlineKeyboardButton(text = text.events_button_text, callback_data = "events")],
    [InlineKeyboardButton(text = text.youth_club_button_text, callback_data = "youth_club")],
    [InlineKeyboardButton(text = text.museum_button_text, callback_data = "museum")],
    [InlineKeyboardButton(text = text.pushkin_card_button_text, callback_data = "pushkin_card")],
    [InlineKeyboardButton(text = text.classes_button_text, callback_data = "classes")]
]
main_menu = InlineKeyboardMarkup(inline_keyboard = main_menu, resize_keyboard = True)

cancel_menu = InlineKeyboardMarkup(inline_keyboard = [[InlineKeyboardButton(text = text.cancel_action, callback_data = "cancel_action")]], resize_keyboard = True)

youth_club_menu = InlineKeyboardMarkup(
    inline_keyboard = [[InlineKeyboardButton(text = text.apply_club_button_text, callback_data = "apply_for_club_membership", resize_keyboard = True)],
                       [InlineKeyboardButton(text = text.to_main_menu, callback_data = "to_main_menu", resize_keyboard = True)]])

def get_classes_list():
    classes_builder = InlineKeyboardBuilder()
    classes_dictionary = db.get_classes()
    try:
        for item in classes_dictionary:
            classes_builder.button(text = item.name, callback_data = CallbackFactory(action = "show_class", id = item.class_id))
    except:
        classes_builder.button(text = text.empty_button_text, callback_data = CallbackFactory(action = "go_back"))
    classes_builder.button(text = text.to_main_menu, callback_data = "to_main_menu")
    classes_builder.adjust(2)
    return classes_builder.as_markup(resize_keyboard = True)

def get_events_list(current_id: Optional[int]):
    events_builder = InlineKeyboardBuilder()
    event_dictionary = db.get_events()
    if current_id != None: 
        events_builder.button(
            text = text.apply_event_button_text.format(name = db.Event.get_by_id(current_id).short_name), 
            callback_data = CallbackFactory(action = "apply_for_event", id = current_id))
    try:
        for item in event_dictionary:
            events_builder.button(text = item.short_name, callback_data = CallbackFactory(action = "show_event", id = item.event_id))
    except:
        events_builder.button(text = text.empty_button_text, callback_data = CallbackFactory(action = "go_back"))
    events_builder.button(text = text.to_main_menu, callback_data = "to_main_menu")
    events_builder.adjust(1)
    return events_builder.as_markup(resize_keyboard = True)
