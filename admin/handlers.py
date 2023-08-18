import asyncio

from contextlib import suppress

from aiogram import types, F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext

from admin.text import *
from admin.kb import *

admin_router = Router()

@admin_router.callback_query(F.data == "to_admin_main_menu")
async def to_admin_main_menu(callback: types.CallbackQuery):
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(text = admin_main_menu, reply_markup = main_menu)
        await callback.answer()

@admin_router.callback_query(F.data == "process_applications")
async def call_process_application_menu(callback: types.CallbackQuery):
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(text = processing_menu, reply_markup = get_applications_kb())
        await callback.answer()

@admin_router.callback_query(F.data == "event_app")
async def event_app(callback: types.CallbackQuery):
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(text = "Оставленные заявки:", reply_markup = get_event_app_kb())
        await callback.answer()

@admin_router.callback_query(F.data == "class_app")
async def class_app(callback: types.CallbackQuery):
    with suppress(TelegramBadRequest):
        await callback.answer()

@admin_router.callback_query(F.data == "club_app")
async def club_app(callback: types.CallbackQuery):
    with suppress(TelegramBadRequest):
        await callback.answer()

@admin_router.callback_query(F.data == "museum_app")
async def museum_app(callback: types.CallbackQuery):
    with suppress(TelegramBadRequest):
        await callback.answer()

@admin_router.callback_query(F.data == "proposal_app")
async def proposal_app(callback: types.CallbackQuery):
    with suppress(TelegramBadRequest):
        await callback.answer()

@admin_router.callback_query(F.data == "go_back_app")
async def go_back_app(callback: types.CallbackQuery):
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(text = processing_menu, reply_markup = get_applications_kb())
        await callback.answer()

@admin_router.callback_query(CallbackFactory.filter(F.action == "show_event_app"))
async def show_event_app(callback: types.CallbackQuery, callback_data: CallbackFactory):
    with suppress(TelegramBadRequest):
        current_application : db.EventApplication = db.EventApplication.get_by_id(callback_data.id)
        await callback.message.edit_text(text = f"{current_application.name}, {current_application.phone}", 
                                         reply_markup = get_actions_kb(callback_data.id))
        await callback.answer()
