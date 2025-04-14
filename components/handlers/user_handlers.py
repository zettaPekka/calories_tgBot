from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from core.init_bot import bot
from components.keyboards.user_kb import start_kb, add_food_kb, back_kb
from components.states.user_states import SendingFood
from ai_api.answer import answer_to_text_prompt, answer_to_view_prompt, answer_to_voice_prompt
from ai_api.data_processing import formatting_data
from database.crud import add_user, add_food


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