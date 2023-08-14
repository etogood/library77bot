from aiogram.types import *
from aiogram.utils.keyboard import *
from aiogram.filters.callback_data import CallbackData
from typing import Optional

import db
import text

from aiogram.types import *

class CallbackFactory(CallbackData, prefix="eventfab"):
    action: str
    id: Optional[int]

main_menu = InlineKeyboardMarkup(
    inline_keyboard = [[InlineKeyboardButton(text = text.schedule_button_text, callback_data = "schedule")],
                       [InlineKeyboardButton(text = text.events_button_text, callback_data = "events")],
                       [InlineKeyboardButton(text = text.youth_club_button_text, callback_data = "youth_club")],
                       [InlineKeyboardButton(text = text.museum_button_text, callback_data = "museum")],
                       [InlineKeyboardButton(text = text.pushkin_card_button_text, callback_data = "pushkin_card")],
                       [InlineKeyboardButton(text = text.classes_button_text, callback_data = "classes")],
                       [InlineKeyboardButton(text = text.partnership_button_text, callback_data = "partnership")],
                       ], resize_keyboard = True)

cancel_menu = InlineKeyboardMarkup(inline_keyboard = [[InlineKeyboardButton(text = text.cancel_action, callback_data = "cancel_action")]], resize_keyboard = True)

youth_club_menu = InlineKeyboardMarkup(
    inline_keyboard = [[InlineKeyboardButton(text = text.apply_club_button_text, callback_data = "apply_for_club_membership", resize_keyboard = True)],
                       [InlineKeyboardButton(text = text.to_main_menu, callback_data = "to_main_menu", resize_keyboard = True)]])

become_partner_menu = InlineKeyboardMarkup(
    inline_keyboard = [[InlineKeyboardButton(text = text.apply_partnership, callback_data = "become_partner", resize_keyboard = True)],
                       [InlineKeyboardButton(text = text.to_main_menu, callback_data = "to_main_menu", resize_keyboard = True)]])

def get_classes_list(current_id: Optional[int]) -> InlineKeyboardMarkup :
    classes_builder = InlineKeyboardBuilder()
    apply_builder = InlineKeyboardBuilder()

    if current_id != None: 
        apply_builder.button(
            text = text.apply_class_button_text.format(name = db.Class.get_by_id(current_id).name), 
            callback_data = CallbackFactory(action = "apply_for_class", id = current_id))

    classes_dictionary = db.get_classes()
    try:
        for item in classes_dictionary:
            classes_builder.button(text = item.name, callback_data = CallbackFactory(action = "show_class", id = item.class_id))
    except:
        classes_builder.button(text = text.empty_button_text, callback_data = CallbackFactory(action = "go_back"))
    classes_builder.adjust(2)

    classes_keyboard = classes_builder.as_markup().inline_keyboard
    apply_keyboard = apply_builder.as_markup().inline_keyboard
    keyboard = apply_keyboard + classes_keyboard + [[InlineKeyboardButton(text = text.to_main_menu, callback_data = "to_main_menu")]]
            
    return InlineKeyboardMarkup(inline_keyboard = keyboard, resize_keyboard = True)

def get_events_list(current_id: Optional[int]) -> InlineKeyboardMarkup :
    events_builder = InlineKeyboardBuilder()

    if current_id != None: 
        events_builder.button(
            text = text.apply_event_button_text.format(name = db.Event.get_by_id(current_id).short_name), 
            callback_data = CallbackFactory(action = "apply_for_event", id = current_id))
        
    try:
        event_dictionary = db.get_events()
        for item in event_dictionary:
            events_builder.button(text = item.short_name, callback_data = CallbackFactory(action = "show_event", id = item.event_id))
    except:
        events_builder.button(text = text.empty_button_text, callback_data = CallbackFactory(action = "go_back"))

    events_builder.button(text = text.to_main_menu, callback_data = "to_main_menu")

    events_builder.adjust(1)
    return events_builder.as_markup(resize_keyboard = True)
