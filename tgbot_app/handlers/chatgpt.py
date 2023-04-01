from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot_app.keyboards.inline import (chatgpt_cd, gen_cancel_kb,
                                        gen_chatgpt_kb, gen_creation_next_kb)
from tgbot_app.loader import dp
from tgbot_app.utils.chatgpt_utils import get_chatgpt_answer
from tgbot_app.utils.database import (get_active_session, reset_messages,
                                      save_msg)


@dp.callback_query_handler(chatgpt_cd.filter(action='make'))
async def chat_gpt_creation(callback: CallbackQuery, callback_data: dict):
    user_id = callback.from_user.id
    markup = await gen_chatgpt_kb(callback_data.get('place'))

    session = await get_active_session(user_id)

    msg = await callback.message.answer(text='Загрузка... Может занять до 1мин...')
    text = await get_chatgpt_answer(user_id)
    await save_msg(user_id, text, is_user=False)

    await msg.edit_text(text=text, reply_markup=markup)


@dp.callback_query_handler(chatgpt_cd.filter(action='specify'))
async def specify_answer(callback: CallbackQuery, state: FSMContext, callback_data: dict):
    place = callback_data.get('place')
    markup = await gen_cancel_kb(place)

    await state.set_state('specify_chatgpt')
    async with state.proxy() as data:
        data['place'] = place

    await callback.message.answer(text='Введите уточнения по вашему запросу:',
                                  reply_markup=markup)
    await callback.answer()


@dp.message_handler(state='specify_chatgpt')
async def set_new_msg(message: Message, state: FSMContext):
    user_id = message.from_user.id
    async with state.proxy() as data:
        place = data['place']

    await save_msg(user_id, message.text, is_user=True)

    msg = await message.answer(text='Загрузка... Может занять до 1мин...')

    text = await get_chatgpt_answer(user_id)
    await save_msg(user_id, text, is_user=False)

    await msg.edit_text(text=text, reply_markup=await gen_chatgpt_kb(place))

    await state.reset_state()


@dp.callback_query_handler(chatgpt_cd.filter(action='reset'))
async def reset_chatgpt(callback: CallbackQuery, callback_data: dict):
    user_id = callback.from_user.id
    place = callback_data.get('place')
    markup = await gen_creation_next_kb() if place == 'creation_next' else 'TODO'

    await reset_messages(user_id)

    await callback.message.answer(text='Диалог с ChatGPT cброшен.', reply_markup=markup)
    await callback.answer()
