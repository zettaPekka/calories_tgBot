from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


start_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отправить', callback_data='send_food'),
        InlineKeyboardButton(text='Профиль', callback_data='profile')]
])

add_food_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сохранить в дневник', callback_data='save_food'),
        InlineKeyboardButton(text='Отмена', callback_data='back')]
])

back_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='back')]
])

def generate_page_keyboard(current_page: int, total_pages: int) -> InlineKeyboardMarkup:
    keyboard = []

    nav_buttons = []
    if current_page > 1:
        nav_buttons.append(InlineKeyboardButton(
            text='⬅️ Назад', 
            callback_data=f'before_page_{current_page}'
        ))
    if current_page < total_pages:
        nav_buttons.append(InlineKeyboardButton(
            text='Вперед ➡️', 
            callback_data=f'after_page_{current_page}'
        ))
    
    if nav_buttons:
        keyboard.append(nav_buttons)
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)