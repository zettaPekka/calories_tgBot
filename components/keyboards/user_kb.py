from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


start_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отправить', callback_data='send_food')]
])

add_food_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сохранить в дневник', callback_data='save_food'),
        InlineKeyboardButton(text='Отмена', callback_data='back')]
])

back_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='back')]
])