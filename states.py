from aiogram.filters.state import State, StatesGroup

class ApplyForClubMembership(StatesGroup):
    fill_name = State()
    fill_phone = State()

class ApplyForEvent(StatesGroup):
    fill_name = State()
    fill_phone = State()

class ApplyForClass(StatesGroup):
    fill_name = State()
    fill_phone = State()

class ApplyForPartnership(StatesGroup):
    fill_proposal = State()