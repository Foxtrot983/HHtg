from aiogram.fsm.state import StatesGroup, State


class Menu(StatesGroup):
    start = State()
    menu = State()
    get_token = State()
    resume_choice = State()
    show_vacancies = State()