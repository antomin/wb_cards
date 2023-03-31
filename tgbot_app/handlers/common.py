from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot_app.keyboards.inline import (cancel_state_cd, gen_chatgpt_kb,
                                        gen_creation_kb, gen_product_kb)
from tgbot_app.loader import dp
from tgbot_app.utils.database import (add_user_session, fetch_data,
                                      get_active_session)
from tgbot_app.utils.seo_utils import get_seo_dictionary, get_word_frequencies
from tgbot_app.utils.text_variables import CREATION_MSG, HELP_PRODUCT
from tgbot_app.utils.values_utils import get_raw_text, update_data


@dp.message_handler(state='change_data')
async def save_fields(message: Message, state: FSMContext):
    user_id = message.from_user.id
    value = message.text
    async with state.proxy() as data:
        field = data.get('field')
        place = data.get('place')

    markup = await gen_creation_kb() if place == 'creation' else await gen_product_kb()

    session = await get_active_session(user_id)
    if not session:
        await add_user_session(user_id, message.from_user.username, {})

    if field == 'sku_plus':
        msg = await message.answer('Загрузка данных...')

        scu_list = [scu.strip() for scu in value.split(',')[:5]]
        await update_data(user_id, 'sku_plus', ', '.join(scu_list))
        raw_text = await get_raw_text(scu_list)

        await msg.edit_text('Загрузка завершена.\nАнализируем ключевые слова...')

        word_frequencies = await get_word_frequencies(raw_text)
        # await update_data(user_id, 'seo_dict', ', '.join(word_frequencies))

        await msg.edit_text('Загрузка завершена.\nСловарь создан.\nВыбираем SEO-фразы...')

        seo_phrases = await fetch_data(word_frequencies)

        await msg.edit_text('Загрузка завершена.\nСловарь создан.\nSEO-фразы выбраны.\nСоставляем Ваш SEO-словарь...')

        seo_dict = await get_seo_dictionary(seo_phrases)
        value = ', '.join(seo_dict)
        await update_data(user_id, 'seo_dict', value)

        await msg.edit_text(text='Ваш SEO-словарь составлен:\n\n' + value, reply_markup=markup)

        await state.reset_state()
        return

    await update_data(user_id, field, value)

    await message.answer('Данные обновлены.', reply_markup=markup)
    await state.reset_state()


@dp.callback_query_handler(cancel_state_cd.filter(), state='*')
async def cancel_changing(callback: CallbackQuery, state: FSMContext, callback_data: dict):
    place = callback_data.get('place')

    if place == 'product':
        markup = await gen_product_kb()
        text = HELP_PRODUCT
    elif place == 'chatgpt':
        markup = await gen_chatgpt_kb()
        text = 'Отменено.'
    elif place == 'creation':
        markup = await gen_creation_kb()
        text = CREATION_MSG
    else:
        markup = None
        text = 'Отменено.'

    await callback.answer()
    await state.reset_state()
    await callback.message.edit_text(text=text, reply_markup=markup, disable_web_page_preview=True)
