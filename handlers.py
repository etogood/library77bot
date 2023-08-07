from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils import markdown

import kb
import text

router = Router()

@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.menu)


@router.message(F.text == "Меню")
@router.message(F.text == "меню")
@router.message(F.text == "Выйти в меню")
@router.message(F.text == "◀️ Выйти в меню")
async def menu(msg: Message):
    await msg.answer(text.menu, reply_markup=kb.menu)


@router.message(F.text == text.schedule_item)
async def schedule(msg: Message):
    await msg.answer(text.schedule, reply_markup=kb.menu)


@router.message(F.text == text.events_item)
async def events(msg: Message):
    await msg.answer("text\.events", reply_markup=kb.menu)


@router.message(F.text == text.youth_club_item)
async def youth_club(msg: Message):
    await msg.answer("text\.youth_club", reply_markup=kb.menu)


router.message(F.text == text.museum_item)
async def museum(msg: Message):
    await msg.answer("text\.museum", reply_markup=kb.menu)


router.message(F.text == text.pushkin_card_item)
async def pushkin_card(msg: Message):
    await msg.answer("text\.pushkin_card", reply_markup=kb.menu)


router.message(F.text == text.classes_item)
async def classes(msg: Message):
    await msg.answer("text\.classes", reply_markup=kb.menu)