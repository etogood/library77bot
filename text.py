import db

greet = "Привет, <b>{name}</b>\n\nЧто тебя интересует?"
menu = "◀️ Вернуться"
classes_menu = "📍 Выберете Интересующий вас кружок"

schedule_item = "📅 Узнать график работы"
events_item = "📆 Мероприятия"
youth_club_item = "🗺️ Молодёжный клуб РГО"
museum_item = "🏺 Музей"
pushkin_card_item = "💳 Пушкинская карта"
classes_item = "🎨 Кружки"


pushkin_card = f"На данный момент, с помощью пушкинской карты лица от 14 лет могут оплачивать:\n<b>{db.get_pushkin_card_classes_list()}</b>"
schedule = "Расписание:\n\nВт-Сб 12:00 — 22:00\nВс 12:00 — 20:00\nПн — выходной"