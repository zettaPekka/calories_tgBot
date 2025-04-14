from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from core.init_bot import bot
from components.keyboards.user_kb import start_kb, add_food_kb, back_kb, generate_page_keyboard
from components.states.user_states import SendingFood
from ai_api.answer import answer_to_text_prompt, answer_to_view_prompt, answer_to_voice_prompt
from ai_api.data_processing import formatting_data
from database.crud import add_user, add_food, get_diary


router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer('привет ты можешь отправь что ты кушал сегодня (текст, гс, фото) по кнопке ниже',
                            reply_markup=start_kb)
    await add_user(tg_id=message.from_user.id)

@router.callback_query(F.data == 'send_food')
async def send_food(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state == 'SendingFood:waiting':
        await callback.message.answer('Дождитесь прошлого запроса')
    else:
        await callback.answer()
        await callback.message.answer('пришлите еду', reply_markup=back_kb)
        await state.set_state(SendingFood.sending)

@router.message(SendingFood.sending)
async def start(message: Message, state: FSMContext):
    if message.content_type == ContentType.TEXT:
        waiting_message = await message.answer('Генерируется...')
        await state.set_state(SendingFood.waiting)
        res = await answer_to_text_prompt(message_text=message.text)
        res = await formatting_data(res)
        if res:
            answer_text = f'Калории:  {res['calories']}\nЖиры: {res['fats']}\nБелки: {res['proteins']}\nУглеводы: {res['carbohydrates']}'
            await message.answer(answer_text, reply_markup=add_food_kb)
            await state.clear()
        else:
            await message.answer('Ошибка, возможно не правильное описание блюда. Попробуйте еще раз')
            await state.set_state(SendingFood.sending)
        await waiting_message.delete()
    elif message.content_type == ContentType.PHOTO:
        waiting_message = await message.answer('Генерируется...')
        await state.set_state(SendingFood.waiting)
        res = await answer_to_view_prompt(message=message)
        res = await formatting_data(res)
        if res:
            answer_text = f'Калории:  {res['calories']}\nЖиры: {res['fats']}\nБелки: {res['proteins']}\nУглеводы: {res['carbohydrates']}'
            await message.answer(answer_text, reply_markup=add_food_kb)
            await state.clear()
        else:
            await message.answer('Ошибка, возможно не правильное описание блюда. Попробуйте еще раз')
            await state.set_state(SendingFood.sending)
        await waiting_message.delete()
    elif message.content_type == ContentType.VOICE:
        waiting_message = await message.answer('Генерируется...')
        await state.set_state(SendingFood.waiting)
        res = await answer_to_voice_prompt(message=message)
        res = await formatting_data(res)
        if res:
            answer_text = f'Калории: {res['calories']}\nЖиры: {res['fats']}\nБелки: {res['proteins']}\nУглеводы: {res['carbohydrates']}'
            await message.answer(answer_text, reply_markup=add_food_kb)
            await state.clear()
        else:
            await message.answer('Ошибка, возможно не правильное описание блюда. Попробуйте еще раз')
            await state.set_state(SendingFood.sending)
        await waiting_message.delete()
    else:
        await message.answer('Бот принимает только текст фото или гс')

@router.callback_query(F.data == 'save_food')
async def save_food(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('Успешно сохранено!', reply_markup=back_kb)
    callories = callback.message.text.split(' ')
    callories = int(callories[2][:-5])
    await add_food(tg_id=callback.message.chat.id, calories=callories)

@router.callback_query(F.data == 'back')
async def back(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text('привет ты можешь отправь что ты кушал сегодня (текст, гс, фото) по кнопке ниже',
                            reply_markup=start_kb)
    await state.clear()

@router.callback_query(F.data == 'profile')
async def profile(callback: CallbackQuery):
    await callback.answer()
    diary = await get_diary(tg_id=callback.message.chat.id)
    
    if not diary:
        await callback.message.answer('Дневник пуст')
        return
    
    answer_text = ['']
    page_index = 0
    for i, (date, calories) in enumerate(diary.items(), 1):
        if i % 15 == 1 and i != 1:
            answer_text.append('')
            page_index += 1
        answer_text[page_index] += f'<b>• {date}</b>\n<i>{calories} ккал</i>\n\n'

    await callback.message.edit_text(
        f'Страница №1/{len(answer_text)}\n\n{answer_text[0]}',
        reply_markup=generate_page_keyboard(1, len(answer_text))
    )


@router.callback_query(F.data.startswith('before_page_'))
async def before_page_index(callback: CallbackQuery):
    await callback.answer()
    try:
        current_page = int(callback.data.split('_')[-1])
        if current_page <= 1:
            await callback.answer('Это первая страница')
            return
        
        diary = await get_diary(tg_id=callback.message.chat.id)
        if not diary:
            return
        
        answer_text = ['']
        page_index = 0
        for i, (date, calories) in enumerate(diary.items(), 1):
            if i % 15 == 1 and i != 1:
                answer_text.append('')
                page_index += 1
            answer_text[page_index] += f'<b>• {date}</b>\n<i>{calories} ккал</i>\n\n'
        
        new_page = current_page - 1
        await callback.message.edit_text(
            f'Страница №{new_page}/{len(answer_text)}\n\n{answer_text[new_page-1]}',
            reply_markup=generate_page_keyboard(new_page, len(answer_text)))
            
    except Exception:
        await callback.answer('Ошибка перехода')

@router.callback_query(F.data.startswith('after_page_'))
async def after_page_index(callback: CallbackQuery):
    await callback.answer()
    try:
        current_page = int(callback.data.split('_')[-1])
        diary = await get_diary(tg_id=callback.message.chat.id)
        if not diary:
            return
        
        answer_text = ['']
        page_index = 0
        for i, (date, calories) in enumerate(diary.items(), 1):
            if i % 15 == 1 and i != 1:
                answer_text.append('')
                page_index += 1
            answer_text[page_index] += f'<b>• {date}</b>\n<i>{calories} ккал</i>\n\n'
        
        if current_page >= len(answer_text):
            await callback.answer('Это последняя страница')
            return
        
        new_page = current_page + 1
        await callback.message.edit_text(
            f'Страница №{new_page}/{len(answer_text)}\n\n{answer_text[new_page-1]}',
            reply_markup=generate_page_keyboard(new_page, len(answer_text)))
            
    except Exception:
        await callback.answer('Ошибка перехода')