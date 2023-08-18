from aiogram.types import *
from aiogram.utils.keyboard import *
from aiogram.filters.callback_data import CallbackData
from typing import Optional

from admin.text import *

import db

class CallbackFactory(CallbackData, prefix="adminfab"):
    action: str
    id: Optional[int]

main_menu = InlineKeyboardMarkup(
    inline_keyboard = [[InlineKeyboardButton(text = process_button_text, callback_data = "process_applications")],
                       [InlineKeyboardButton(text = edit_info_button_text, callback_data = "edit_info")]
                       ], resize_keyboard = True)

def get_applications_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard = [[InlineKeyboardButton(text = f"Мероприятия ({len(db.EventApplication)})", callback_data = "event_app")],
                                                    [InlineKeyboardButton(text = f"Кружки ({len(db.ClassApplication)})", callback_data = "class_app")],
                                                    [InlineKeyboardButton(text = f"Клуб РГО ({len(db.YouthClubApplication)})", callback_data = "club_app")],
                                                    [InlineKeyboardButton(text = f"Музей ({len(db.MuseumApplication)})", callback_data = "museum_app")],
                                                    [InlineKeyboardButton(text = f"Партнёрство ({len(db.Proposal)})", callback_data = "proposal_app")],
                                                    [InlineKeyboardButton(text = to_admin_main_menu, callback_data = "to_admin_main_menu")],
                                                    ], resize_keyboard = True)

def get_actions_kb(id: int) -> InlineKeyboardMarkup :
    kb_builder = InlineKeyboardBuilder()

    kb_builder.button(text = "✅ Принять", callback_data = CallbackFactory(action = "accept", id = id))
    kb_builder.button(text = "❌ Отклонить", callback_data = CallbackFactory(action = "decline", id = id))
    kb_builder.button(text = go_back, callback_data = CallbackFactory(action = "go_back"))
    kb_builder.adjust(2)

    return kb_builder.as_markup()


def get_event_app_kb() -> InlineKeyboardMarkup :
    event_app_builder = InlineKeyboardBuilder()

    for app in db.EventApplication:
        event_app_builder.button(text = app.name, callback_data = CallbackFactory(action = "show_event_app", id = app.application_id))
    
    event_app_builder.button(text = go_back, callback_data = "go_back_app")
    event_app_builder.adjust(1)

    return event_app_builder.as_markup(resize_keyboard = True)

