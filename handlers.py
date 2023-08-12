import asyncio

from contextlib import suppress

from aiogram import types, F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext

import kb
import db
import text
import states

basic_router = Router()
club_application_router = Router()


# Menu ----------------------------------------------------------------------------------------------------

# /start
@basic_router.message(Command("start"))
@basic_router.message(Text(text="старт", ignore_case=True))
async def cmd_start(msg: Message):
    await msg.answer(text.greet.format(name = msg.from_user.full_name), reply_markup = kb.main_menu)


@basic_router.message(Command("menu"))
@basic_router.message(Text(text="меню", ignore_case=True))
async def cmd_menu(msg: Message):
    await msg.answer(text.main_menu, reply_markup = kb.main_menu)

# Отмена
@basic_router.callback_query(F.data == "cancel_action")
async def main_menu(callback: types.CallbackQuery, state: FSMContext):
    with suppress(TelegramBadRequest):
        await state.clear()
        await callback.message.edit_text(text = "❌ Действие отменено")
        await callback.answer()
        await asyncio.sleep(1)
        await callback.message.delete()

# Главное меню
@basic_router.callback_query(F.data == "to_main_menu")
async def main_menu(callback: types.CallbackQuery, state: FSMContext):
    with suppress(TelegramBadRequest):
        await state.clear()
        await callback.message.edit_text(text = text.main_menu, reply_markup = kb.main_menu)
        await callback.answer()

# Расписание
@basic_router.callback_query(F.data == "schedule")
async def schedule(callback: types.CallbackQuery):
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(text.schedule, reply_markup = kb.main_menu)
        await callback.answer()

# Мероприятия
@basic_router.callback_query(F.data == "events")
async def events(callback: types.CallbackQuery):
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(text.events, reply_markup = kb.get_events_list())
        await callback.answer()

# Молодёжный клуб РГО
@basic_router.callback_query(F.data == "youth_club")
async def youth_club(callback: types.CallbackQuery):
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(text.youth_club, reply_markup = kb.youth_club_menu)
        await callback.answer()

# Музей
@basic_router.callback_query(F.data == "museum")
async def museum(callback: types.CallbackQuery):
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(text.empty_button_text, reply_markup = kb.main_menu)
        await callback.answer()

# Пушкинская карта
@basic_router.callback_query(F.data == "pushkin_card")
async def pushkin_card(callback: types.CallbackQuery):
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(text.pushkin_card, reply_markup = kb.main_menu)
        await callback.answer()

# Кружки
@basic_router.callback_query(F.data == "classes")
async def classes(callback: types.CallbackQuery):
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(text.classes_menu, reply_markup = kb.get_classes_list())
        await callback.answer()


# FSM ----------------------------------------------------------------------------------------------------

#region FSM Оформление заявки на вступление в молодёжный клуб РГО 

@club_application_router.callback_query(F.data == "apply_for_club_membership")
async def apply_for_club_membership(callback: types.CallbackQuery, state: FSMContext):
    with suppress(TelegramBadRequest):
        await callback.message.answer(text = "Введите своё полное имя:", reply_markup = kb.return_menu)
        await state.set_state(states.ApplyForClubMembership.fill_name)
        await callback.answer(text="Оформление заявки начато")

@club_application_router.message(states.ApplyForClubMembership.fill_name, F.text.regexp(r"^([а-яёА-ЯЁ ]+)$"))
async def name_filled(message: Message, state: FSMContext):
    await state.update_data(filled_name = message.text)
    await message.answer(text = "Теперь введите ваш номер телефона:", reply_markup = kb.return_menu)
    await state.set_state(states.ApplyForClubMembership.fill_phone)

@club_application_router.message(states.ApplyForClubMembership.fill_name)
async def name_filled_incorrectly(message: Message):
    await message.answer(text = "Имя не должно содержать лишних символов\n\nПопробуйте ввести своё имя ещё раз:", reply_markup = kb.return_menu)

@club_application_router.message(states.ApplyForClubMembership.fill_phone, F.text.regexp(r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$"))
async def phone_filled(message: Message, state: FSMContext):
    await state.update_data(filled_phone = message.text)
    user_data = await state.get_data()
    db.YouthClubApplication.create(name = user_data['filled_name'], phone = user_data['filled_phone'])
    await message.answer(
        text = f"Ваша заявка сформирована: {user_data['filled_name']}, {user_data['filled_phone']}!\n\nОжидайте ответа в личные сообщения")
    await state.clear()
    await message.answer(text.main_menu, reply_markup = kb.main_menu)

@club_application_router.message(states.ApplyForClubMembership.fill_phone)
async def phone_filled_incorrectly(message: Message):
    await message.answer(text="Неверный формат номера телефона\n\nПопробуйте ввести номер телефона ещё раз:", reply_markup = kb.return_menu)

#endregion

#region Buttons factory filters (Мероприятия, кружки) ----------------------------------------------------------------------------------------------------
async def send_event_info(message: types.Message, text: str):
    with suppress(TelegramBadRequest):
        await message.edit_text(text = text, reply_markup = kb.get_events_list())

@basic_router.callback_query(kb.CallbackFactory.filter(F.action == "show_event"))
async def callbacks_show_event_fab(callback: types.CallbackQuery, callback_data: kb.CallbackFactory):
    with suppress(TelegramBadRequest):
        await send_event_info(callback.message, db.get_full_event_text(callback_data.id))
        await callback.answer()

async def send_class_info(message: types.Message, text: str, callback_data: kb.CallbackFactory):
    with suppress(TelegramBadRequest):
        await message.edit_text(text = text, reply_markup = kb.get_classes_list())
        pics = db.get_class_pictures(callback_data.id)
        if pics != None: await message.answer_media_group(media = pics)

        
@basic_router.callback_query(kb.CallbackFactory.filter(F.action == "show_class"))
async def callbacks_show_class_fab(callback: types.CallbackQuery, callback_data: kb.CallbackFactory):
    with suppress(TelegramBadRequest):
        await send_class_info(callback.message, db.get_full_class_text(callback_data.id), callback_data)
        await callback.answer()

@basic_router.callback_query(kb.CallbackFactory.filter(F.action == "go_back"))
async def callbacks_go_back_fab(callback: types.CallbackQuery):
    with suppress(TelegramBadRequest):
        await callback.answer("Ничего не найдено")

#endregion