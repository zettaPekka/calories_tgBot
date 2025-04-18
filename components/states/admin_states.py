from aiogram.fsm.state import State, StatesGroup


class EditText(StatesGroup):
    start = State()
    error = State()
    help = State()
    image = State()