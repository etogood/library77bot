import db

greet = "Привет, <b>{name}</b>\n\nЧто тебя интересует?"
menu = "◀️ Вернуться"
classes_menu = "📍 Выберете Интересующий вас кружок"

empty_button_text = "Тут пусто 🧐"

schedule_button_text = "📅 Узнать график работы"
events_button_text = "📆 Мероприятия"
youth_club_button_text = "🗺️ Молодёжный клуб РГО"
museum_button_text = "🏺 Музей"
pushkin_card_button_text = "💳 Пушкинская карта"
classes_button_text = "🎨 Кружки"


pushkin_card = f"На данный момент, с помощью пушкинской карты лица от 14 лет могут оплачивать:\n<b>{db.get_pushkin_card_classes_list()}</b>"
schedule = "Расписание:\n\nВт-Сб 12:00 — 22:00\nВс 12:00 — 20:00\nПн — выходной"