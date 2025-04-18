from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


options_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Приветствие', callback_data='change_start')],
    [InlineKeyboardButton(text='Ошибка', callback_data='change_error')],
    [InlineKeyboardButton(text='Помощь', callback_data='change_help')],
    [InlineKeyboardButton(text='Картинка помощи', callback_data='change_image')]
])

back_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отмена', callback_data='back')]
])