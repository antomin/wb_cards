from aiogram.types import CallbackQuery, Message

from tgbot_app.keyboards.inline import (gen_product_kb, gen_update_kb,
                                        main_menu_cd, update_cd)
from tgbot_app.loader import dp
from tgbot_app.utils.database import reset_messages, update_field_session


@dp.message_handler(commands=['reset'])
@dp.callback_query_handler(main_menu_cd.filter(action='update'))
async def product_handler(callback: CallbackQuery | Message):
    if isinstance(callback, CallbackQuery):
        await callback.message.edit_text(
            text='ВНИМАНИЕ!!!\nОбновление удалит все раннее загруженные данные.\nВы уверены?',
            reply_markup=await gen_update_kb()
        )
        return

    await callback.answer(
        text='ВНИМАНИЕ!!!\nОбновление удалит все раннее загруженные данные.\nВы уверены?',
        reply_markup=await gen_update_kb()
    )


@dp.callback_query_handler(update_cd.filter())
async def update_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    await update_field_session(user_id, 'is_active', False)
    await reset_messages(user_id)
    await callback.message.edit_text(
        text='Данные успешно очищены.',
        reply_markup=await gen_product_kb()
    )
