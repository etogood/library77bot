from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
menu = [
    [InlineKeyboardButton(text="📅 Узнать график работы", callback_data="schedule"),
    InlineKeyboardButton(text="📆 Мероприятия", callback_data="events")],
    [InlineKeyboardButton(text="🗺️ Молодёжный клуб РГО", callback_data="youth_club"),
    InlineKeyboardButton(text="🏺 Музей", callback_data="museum")],
    [InlineKeyboardButton(text="💳 Пушкинская карта", callback_data="pushkin_card"),
    InlineKeyboardButton(text="🎨 Кружки", callback_data="classes")]
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)
exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)
iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])

