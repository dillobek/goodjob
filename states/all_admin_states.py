from aiogram.dispatcher.filters.state import State, StatesGroup

class Admin_Access(StatesGroup):
    admin_panel = State ()
    get_new_course_name = State()
    get_new_course_video = State ()
    get_new_course_description = State()

class post_send(StatesGroup):
    post = State ()

class social(StatesGroup):
    get_name=State()
    get_pdf=State()
    get_description=State()