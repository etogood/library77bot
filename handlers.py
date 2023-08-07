from aiogram import types, F, Router
from aiogram.types import Message
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext

import kb
import db
import text
import states

basic_router = Router()
club_application_router = Router()

# Replies ----------------------------------------------------------------------------------------------------

# /start
@basic_router.message(Command("start"))
@basic_router.message(Text(text="старт", ignore_case=True))
async def cmd_start(msg: Message):
    await msg.answer(text.greet.format(name = msg.from_user.full_name), reply_markup = kb.main_menu)

# /cancel
@basic_router.message(Command(commands=["cancel"]))
@basic_router.message(Text(text="отмена", ignore_case=True))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text="Действие отменено", reply_markup = kb.main_menu)

# Главное меню
@basic_router.message(Text(text.main_menu))
async def main_menu(msg: Message, state: FSMContext):
    await msg.answer("Что вас интересует?", reply_markup = kb.main_menu)
    await state.clear()

# Расписание
@basic_router.message(Text(text.schedule_button_text))
async def schedule(msg: Message):
    await msg.answer(text.schedule, reply_markup = kb.main_menu)

# Мероприятия
@basic_router.message(Text(text.events_button_text))
async def events(msg: Message):
    await msg.answer(text.empty_button_text, reply_markup = kb.main_menu)

# Молодёжный клуб РГО
@basic_router.message(Text(text.youth_club_button_text))
async def youth_club(msg: Message):
    await msg.answer(text.youth_club, reply_markup = kb.youth_club_menu)

# Музей
@basic_router.message(Text(text.museum_button_text))
async def museum(msg: Message):
    await msg.answer(text.empty_button_text, reply_markup = kb.main_menu)

# Пушкинская карта
@basic_router.message(Text(text.pushkin_card_button_text))
async def pushkin_card(msg: Message):
    await msg.answer(text.pushkin_card, reply_markup = kb.main_menu)

# Кружки
@basic_router.message(Text(text.classes_button_text))
async def classes(msg: Message):
    await msg.answer(text.classes_menu, reply_markup = kb.classes_menu)


# Inlines ----------------------------------------------------------------------------------------------------

@club_application_router.callback_query(F.data == "apply_for_club_membership")
async def apply_for_club_membership(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(text = "Введите своё полное имя:", reply_markup = kb.return_menu)
    await state.set_state(states.ApplyForClubMembership.fill_name)
    await callback.answer(text="Оформление заявки начато")

@club_application_router.message(states.ApplyForClubMembership.fill_name, F.text.regexp(r"^([а-яёА-ЯЁ ]+)$"))
async def name_filled(message: Message, state: FSMContext):
    await state.update_data(filled_name = message.text)
    await message.answer(text = "Теперь введите ваш возраст:")
    await state.set_state(states.ApplyForClubMembership.fill_age)

@club_application_router.message(states.ApplyForClubMembership.fill_name)
async def name_filled_incorrectly(message: Message):
    await message.answer(text = "Имя не должно содержать лишних символов\n\nПопробуйте ввести своё имя ещё раз:")

@club_application_router.message(states.ApplyForClubMembership.fill_age, F.text.regexp(r"^(\d+)$"))
async def age_filled(message: Message, state: FSMContext):
    await state.update_data(filled_age = message.text)
    user_data = await state.get_data()
    db.YouthClubApplication.create(name=user_data['filled_name'], age=user_data['filled_age'])
    await message.answer(
        text = f"Ваша заявка сформирована: {user_data['filled_name']}, {user_data['filled_age']}!\n\nОжидайте ответа от руководителя в личные сообщения",
        reply_markup = kb.main_menu)
    await state.clear()

@club_application_router.message(states.ApplyForClubMembership.fill_age)
async def age_filled_incorrectly(message: Message):
    await message.answer(text="Значение возраста должно содержать одно число\n\nПопробуйте ввести свой возраст ещё раз:")