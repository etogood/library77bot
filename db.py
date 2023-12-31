from peewee import *
from aiogram.types import FSInputFile, InputMediaPhoto
from contextlib import suppress

import os.path
import time

db = SqliteDatabase("db.sqlite")

class BaseModel(Model):
    class Meta:
        database = db

#region Tables

# Мероприятия
class Event(BaseModel):
    event_id = AutoField(column_name="EventId")
    name = TextField(column_name="Name", null=True)
    short_name = TextField(column_name="ShortName", null=True)
    text = TextField(column_name="Text", null=True)
    is_free = BooleanField(column_name="IsFree", null=True)
    cost = TextField(column_name="Cost", null=True)
    date = TextField(column_name="Date", null=True)
    address = TextField(column_name="Address", null=True)
    age_cens = TextField(column_name="AgeCens", null=True)

    class Meta:
        table_name = 'Events'

# Запись на мероприятие
class EventApplication(BaseModel):
    application_id = AutoField(column_name="ApplicationId")
    event_id = ForeignKeyField(Event, column_name="EventId")
    name = TextField(column_name="Name", null=False)
    phone = TextField(column_name="Phone", null=True)

    class Meta:
        table_name = 'EventApplications'

# Кружки
class Class(BaseModel):
    class_id = AutoField(column_name="ClassId")
    name = TextField(column_name="Name", null=True)
    text = TextField(column_name="Text", null=True)
    picture = TextField(column_name="PicturePath", null=True)
    is_on_pushkin_card = BooleanField(column_name="IsOnPushkinCard", null=False)
    is_for_kids = BooleanField(column_name="IsForKids", null=False)

    class Meta:
        table_name = 'Classes'

# Запись в кружок
class ClassApplication(BaseModel):
    application_id = AutoField(column_name="ApplicationId")
    class_id = ForeignKeyField(Class, column_name="ClassId")
    name = TextField(column_name="Name", null=False)
    phone = TextField(column_name="Phone", null=True)

    class Meta:
        table_name = 'ClassApplications'

# Запись в клуб РГО
class YouthClubApplication(BaseModel):
    application_id = AutoField(column_name="ApplicationId")
    name = TextField(column_name="Name", null=False)
    phone = TextField(column_name="Phone", null=True)

    class Meta:
        table_name = 'YouthClubApplications'

# Экскурсия / музей
class Museum(BaseModel):
    museum_id = AutoField(column_name="MuseumId")
    name = TextField(column_name="Name", null=True)
    decription = TextField(column_name="Decription", null=True)

    class Meta:
        table_name = 'Museums'

# Запись на экскурсию
class MuseumApplication(BaseModel):
    application_id = AutoField(column_name="ApplicationId")
    museum_id = ForeignKeyField(Museum, column_name="MuseumId")
    name = TextField(column_name="Name", null=True)
    phone = TextField(column_name="Phone", null=True)

    class Meta:
        table_name = "MuseumApplications"

# Предложения партнёрства
class Proposal(BaseModel):
    proposal_id = AutoField(column_name="ProposalId")
    text = TextField(column_name="Text", null=False)

    class Meta:
        table_name = "Proposals"

#endregion

#region Methods

def get_classes():
    return Class.select()

def get_events():
    return Event.select()

def get_pushkin_card_classes_list():
    s = ''
    query = Class.select(Class.name).where(Class.is_on_pushkin_card == True)
    for item in query:
        s += "\n• " + item.name
    return s

def get_full_event_text(id: int):
    event = Event.get_by_id(id)
    text = '<b>' + str(event.name) + '</b>'\
    + '\n\n' + str(event.text)\
    + '\n\n' + "Стоимость посещения: "\
    + (str(event.cost), "бесплатно")[event.is_free]\
    + '\n\n' + str(event.date)\
    + '\n\n' + str(event.address)\
    + '\n\n' + str(event.age_cens)
    return text

def get_full_class_text(id: int):
    clss = Class.get_by_id(id)
    text = '<b>' + str(clss.name) + '</b>'\
    + '\n\n' + str(clss.text)\
    + '\n\n' + ('', "<i>Доступно по пушкинской карте</i>")[clss.is_on_pushkin_card]
    return text

def get_class_pictures(id: int):
    with suppress(AttributeError):
        clss = Class.get_by_id(id)
        files = []
        pics = clss.picture.split(',')
        for pic in pics:
            files.append(InputMediaPhoto(media = FSInputFile("resources/" + pic)))
        return files

#endregion

if not os.path.exists('db.sqlite'):
    Event.create_table()
    EventApplication.create_table()
    Class.create_table()
    ClassApplication.create_table()
    YouthClubApplication.create_table()
    Museum.create_table()
    MuseumApplication.create_table()
    Proposal.create_table()

#region Backup
# Class.create(name="EVERYDAY ENGLISH. KIDS", 
#              text="Изучение бытового и разговорного английского с помощью фильмов, игр и мультиков. Полное погружение в процесс обучения – все общение будет проходить преимущественно на английском языке. \n\nИзучим сленг, идиомы и цитаты. Нескучный английский. \n\nКаждое воскресенье. 12:00-13:00. Дети 6-13 лет. Стоимость 800 р.\n\nАбонемент 3200\n\nНачало 3 сентября.", 
#              picture="everyday_english.jpg", 
#              is_on_pushkin_card=True,
#              is_for_kids=True)
# Class.create(name="EVERYDAY ENGLISH", 
#              text="Изучение бытового и разговорного английского с помощью фильмов, музыки и сериалов . Полное погружение в процесс обучения – все общение будет проходить преимущественно на английском языке. \n\nИзучим сленг, идиомы и цитаты. Нескучный английский.\n\nКаждое воскресенье. 13:15-14:15. От 14 лет. Стоимость 800 р.\n\nАбонемент 3200\n\nНачало 3 сентября.", 
#              picture="everyday_english.jpg",
#              is_on_pushkin_card=True,
#              is_for_kids=False)
# Class.create(name="Зажигай!", 
#              text="Мастер-классы по модельному искусству для детей. Самопрезентация, танцы, модельные проходки, составление, подбор образов и позирование. Все это будет проводиться в игре, так участники смогут усвоить все полученные знания без скуки. В интерактивной лекции, включенной в мастер-класс, ребята будут познавать понятие \"красота\": что это такое, как это понятие развивалось и какие разные определения этого понятие в разных культурах сейчас.\n\nКаждое воскресенье. 14:30-15:45. 6-13 лет. Стоимость 1000 р.\n\nАбонемент 4000\n\nНачало 3 сентября.", 
#              picture="models.jpg",
#              is_on_pushkin_card=False,
#              is_for_kids=True)
# Class.create(name="Школа эстетики", 
#              text="Мастер-классы по модельному искусству. Участники будут пробовать себя в разных сферах: самопрезентация, танцы, модельные проходки, составление, подбор образов и позирование. Также для взрослой аудитории будут проводится занятия по различным сторонам эстетики: парфюмерия, образы, цвета и искусство в целом. Также в мастер-класс будут включены такие аспекты как: фотопозирование, рабочие стороны тела, создание портфолио, работа на публике, раскрепощение и снятие блоков, самовыражение и создание собственного стиля.\n\nКаждое воскресенье. 16:00-17:15. От 14 лет. Стоимость 1000 р.\n\nАбонемент 4000\n\nНачало 3 сентября.", 
#              picture="aesthetics.jpg",
#              is_on_pushkin_card=True,
#              is_for_kids=False)
# Class.create(name="Белый мишка", 
#              text="Клуб юного полярника. Набираем 2 потока: 1 – ранее развитие 4+ (если ребенок интересующийся, то 3+) и 2- старший 7+. Программа о том, что как стать ученым-супергероем. У участников будет Бортовой журнал, который ребята будут заполнять в течение своих экспериментов и исследований. Направления: окружающий мир, география, экология, различные направления, связанные с Арктикой и коренными народами севера. В конце года по итогам исследований будет выпущен журнал с научными статьями участников. Запланированы различные поездки и походы\n\n2 среды каждого месяца (может меняться). В основном 2 и 4 среда. \n\n1 группа 16:00-17:00, 2 группа 17:00-18:00.\n\nСтоимость 10 000 за 8 месяцев.  Разово – 700 р занятие.\n\nНачало 27 сентября.", 
#              picture="white_bear.jpg",
#              is_on_pushkin_card=False,
#              is_for_kids=True)
# Class.create(name="Подготовка к школе", 
#              text="Для каждой группы будут проводится 2 занятия с перерывом: развитие речи и математика. \n\n2 группы: 5-6 лет и 6-7 лет.\n\nРасписание: по субботам 1 гр 12:00 до 13:00; 2 гр 13:30-15:00\n\nСтоимость младшей группы 3500 за месяц.\n\nСтоимость старшей группы 4000 за месяц.\n\nНачало 2 сентября.", 
#              picture = "school_prep.jpg",
#              is_on_pushkin_card=False,
#              is_for_kids=True)
# Class.create(name="Подсекай", 
#              text="Изучение теории и практики рыболовного дела. Все дисциплины спортивного рыболовства: поплавок, донная удочка, спиннинговая ловля, мормышка, карповая ловля. Занятия с детьми проводятся в формате мастер-классов с ведущими рыболовами-спортсменами страны, а также будут тренировочные выезды на рыбалку с опытными наставниками. Руководитель клуба – чемпион мира и главный тренер сборной России по ловле донной удочкой – Алексей Крючков.\n\nВозраст 7-16 лет.\n\nРасписание: каждый четверг 17:00-18:30.\n\nСтоимость абонемента 2000 руб в месяц. Разово – 500р.",
#              is_on_pushkin_card=False,
#              is_for_kids=False)
# Class.create(name="Выстрел", 
#              text="Стрелковый клуб. Развитие спортивных достижений в практической стрельбе, стрелковой подготовке, приобретение навыков безопасного обращения с оружием и понимание культуры стрельбы. Руководитель Косоруков Родион Игоревич.\n\nВозраст от 10 до 18 лет.\n\nРасписание среда, пятница 15:00-15:30, потом теория.\n\nСтоимость 300р за занятие.\n\nАбонемент 2400\n\nНачало занятий 6 сентября.",
#              is_on_pushkin_card=False,
#              is_for_kids=False)
# Class.create(name="Творческая мастерская", 
#              text="*Аистенок* – изо-студия. Рисование в разных техниках и разными материалами. Культура изобразительного искусства. \n\nДети 4-6 лет и 7-9 лет. \n\nРасписание: среда пятница. Мл.гр. 16:30 – 17:10, ст.гр. 17:30 – 18:30.\n\nСтоимость: 1 группа 5000 руб. за месяц (разово 700р). 2 гр 6000 руб. за месяц.(разово 800р).\n\nНачало занятий 6 сентября.\n\n\n*Вязание* – крючком. Схемы, правильная постановка рук, освоение техники вязания крючком.\n\nВозраст: 10-18 лет.\n\nРасписание: среда, пятница  18:30-19:30.\n\nСтоимость 6000 месяц, разово 800р\n\nНачало 6 сентября.", 
#              picture="izo.jpg,knitting.jpg",
#              is_on_pushkin_card=False,
#              is_for_kids=True)
# Class.create(name="Театральная мастерская", 
#              text="Освоение техники традиционного кукольного театра. Направления: Сценическая речь, актерское мастерство, создание кукол, постановка спектаклей, создание декораций, создание и постановка этюдов. \n\nВозраст 9-18 лет. (можно раньше по собеседованию с преподавателем)\n\nРасписание: вторник, пятница 17:00-18:30.\n\nСтоимость 8000 месяц (1400 разово).\n\nНачало 5 сентября.", 
#              picture="dolls.jpg",
#              is_on_pushkin_card=False,
#              is_for_kids=True)
# Class.create(name="Звукорежиссура", 
#              text="Мастер-классы по звукозаписи, мк по созданию музыкальных треков, участие в концертных мероприятиях, в театральном спектакле, мастер-класс по саунд-дизайну для видео. \n\nВозраст от 11 лет.\n\nРасписание: суббота 19:00-20:00.\n\nСтоимость 700 р за занятие.\n\nАбонемент 2800\n\nНачало 2 сентября.", 
#              picture="sound.jpg",
#              is_on_pushkin_card=True,
#              is_for_kids=False)
# Class.create(name="Китайский язык", 
#              text="Основы китайского языка, знакомство с китайской культурой и написанием иероглифов. \n\nВозраст: мл гр. 10-14 лет, от 14 лет\n\nРасписание: воскресенье мл гр 12:30 до 13:30, с 14:00 до 15:00.\n\nСтоимость разово 800 р, абонемент 3200. \n\nНачало 3 сентября", 
#              picture="chinese.jpg",
#              is_on_pushkin_card=True,
#              is_for_kids=False)
#endregion

db.close()