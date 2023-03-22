from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot_app.common.database import (get_active_session, reset_messages,
                                       save_msg, update_field_session)
from tgbot_app.common.text_variables import HELP_CHATGPT, STYLE_DESC
from tgbot_app.common.utils import get_chatgpt_answer
from tgbot_app.keyboards.inline import (chatgpt_cd, chatgpt_style_cd,
                                        gen_cancel_kb, gen_chatgpt_kb,
                                        gen_chatgpt_style_kb,
                                        gen_chatgpt_sub_kb, main_menu_cd)
from tgbot_app.loader import dp


@dp.callback_query_handler(main_menu_cd.filter(action='chatgpt'))
async def chatgpt_main(callback: CallbackQuery | Message):
    session = await get_active_session(callback.from_user.id)

    if not session:
        await callback.message.edit_text(
            text='Не загружено никакой информации о товаре.\nПройдите в раздел Товар и добавьте информацию.',
            reply_markup=await gen_chatgpt_kb(session=False)
        )
        return

    markup = await gen_chatgpt_kb()
    await callback.message.edit_text(text=HELP_CHATGPT, reply_markup=markup)


@dp.callback_query_handler(chatgpt_cd.filter(action='make'))
@dp.callback_query_handler(chatgpt_cd.filter(action='make_seo'))
async def chat_gpt_creation(callback: CallbackQuery, callback_data: dict):
    user_id = callback.from_user.id

    session = await get_active_session(user_id)
    add_seo = True if callback_data.get('action') == 'make_seo' else False

    if add_seo and not session.seo_plus:
        await callback.message.edit_text(
            text='Нет информации SEO+.\nПройдите в раздел Товар и добавьте информацию.',
            reply_markup=await gen_chatgpt_kb(session=False)
        )
        return

    markup = await gen_chatgpt_sub_kb()

    await callback.message.edit_text('Загрузка... Может занять до 1мин...')
    text = await get_chatgpt_answer(user_id, add_seo)
    await save_msg(user_id, text, is_user=False)

    await callback.message.edit_text(text=text, reply_markup=markup)


@dp.callback_query_handler(chatgpt_cd.filter(action='specify'))
async def specify_answer(callback: CallbackQuery, state: FSMContext):
    await state.set_state('specify_chatgpt')
    msg = await callback.message.edit_text(text='Введите уточнения по вашему запросу:',
                                           reply_markup=await gen_cancel_kb('chatgpt'))

    async with state.proxy() as data:
        data['prev_message_id'] = msg.message_id

    await callback.answer()


@dp.message_handler(state='specify_chatgpt')
async def set_new_msg(message: Message, state: FSMContext):
    user_id = message.from_user.id

    async with state.proxy() as data:
        prev_message_id = data['prev_message_id']

    await save_msg(user_id, message.text, is_user=True)

    await message.delete()

    await dp.bot.edit_message_text(
        text='Загрузка... Может занять до 1мин...',
        chat_id=message.chat.id,
        message_id=prev_message_id,
    )

    text = await get_chatgpt_answer(user_id)
    await save_msg(user_id, text, is_user=False)

    await dp.bot.edit_message_text(
        text=text,
        chat_id=message.chat.id,
        message_id=prev_message_id,
        reply_markup=await gen_chatgpt_sub_kb()
    )

    await state.reset_state()


@dp.callback_query_handler(chatgpt_cd.filter(action='reset'))
async def reset_chatgpt(callback: CallbackQuery):
    user_id = callback.from_user.id
    markup = await gen_chatgpt_kb()

    await reset_messages(user_id)

    await callback.message.edit_text(text='Диалог с ChatGPT cброшен.', reply_markup=markup)


@dp.callback_query_handler(chatgpt_cd.filter(action='style'))
async def chatgpt_style(callback: CallbackQuery):
    markup = await gen_chatgpt_style_kb()

    await callback.message.edit_text(text=STYLE_DESC, reply_markup=markup)


@dp.callback_query_handler(chatgpt_style_cd.filter())
async def set_chatgpt_style(callback: CallbackQuery, callback_data: dict):
    style = callback_data.get('value')
    markup = await gen_chatgpt_kb()

    await update_field_session(callback.from_user.id, 'style', style)

    await callback.message.edit_text(text=f'{style.title()} стиль установлен.', reply_markup=markup)
