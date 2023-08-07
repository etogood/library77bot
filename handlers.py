from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command

import kb
import text
import db

router = Router()

@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.main_menu)

@router.message(F.text == text.menu)
async def menu(msg: Message):
    await msg.answer("Что вас интересует?", reply_markup=kb.main_menu)

# Расписание
@router.message(F.text == text.schedule_item)
async def schedule(msg: Message):
    await msg.answer(text.schedule, reply_markup=kb.main_menu)

# Мероприятия
@router.message(F.text == text.events_item)
async def events(msg: Message):
    await msg.answer("text\.events", reply_markup=kb.main_menu)

# Молодёжный клуб РГО
@router.message(F.text == text.youth_club_item)
async def youth_club(msg: Message):
    await msg.answer("text\.youthclub", reply_markup=kb.main_menu)

# Музей
@router.message(F.text == text.museum_item)
async def museum(msg: Message):
    await msg.answer("text\.museum", reply_markup=kb.main_menu)

# Пушкинская карта
@router.message(F.text == text.pushkin_card_item)
async def pushkin_card(msg: Message):
    await msg.answer(text.pushkin_card, reply_markup=kb.main_menu)

# Кружки
@router.message(F.text == text.classes_item)
async def classes(msg: Message):
    await msg.answer(text.classes_menu, reply_markup=kb.classes_menu)