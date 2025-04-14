from aiogram.fsm.state import State, StatesGroup


class SendingFood(StatesGroup):
    sending = State()
    waiting = State()