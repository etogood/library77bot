from aiogram.filters.state import State, StatesGroup

class ApplyForClubMembership(StatesGroup):
    fill_name = State()
    fill_age = State()