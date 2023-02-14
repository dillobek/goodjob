from aiogram.dispatcher.filters.state import State, StatesGroup


class UserState(StatesGroup):
    name = State()
    year = State()
    phone = State()
    sphone = State()
    job = State()
    jobexperience = State()
    salary = State()
    about = State()
    region = State()
    photo = State()
    check = State()

class VacancyState(StatesGroup):
    cname = State()
    type = State()
    job = State()
    jobexperience = State()
    phone = State()
    sphone = State()
    salary = State()
    region = State()
    about = State()
    admin = State()
    photo = State()
    check = State()