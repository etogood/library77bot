import db

greet = "Привет, *{name}*\n\nЧто тебя интересует?"
menu = "📍 Главное меню"

schedule_item = "📅 Узнать график работы"
events_item = "📆 Мероприятия"
youth_club_item = "🗺️ Молодёжный клуб РГО"
museum_item = "🏺 Музей"
pushkin_card_item = "💳 Пушкинская карта"
classes_item = "🎨 Кружки"

pushkin_card = f"С помощью пушкинской карты лица от 14 лет могут оплачивать:\n{db.get_pushkin_card_classes_list()}"
schedule = "Расписание:\n\nВт\-Сб 12:00 — 22:00\nВс 12:00 — 20:00\nПн — выходной"