from aiogram.types import CallbackQuery

from tgbot_app.common.database import update_field_session
from tgbot_app.keyboards.inline import (gen_product_kb, gen_update_kb,
                                        main_menu_cd, update_cd)
from tgbot_app.loader import dp


@dp.callback_query_handler(main_menu_cd.filter(action='update'))
async def product_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        text='ВНИМАНИЕ!!!\nОбновление удалит все раннее загруженные данные.\nВы уверены?',
        reply_markup=await gen_update_kb()
    )


@dp.callback_query_handler(update_cd.filter())
async def update_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    await update_field_session(user_id, 'is_active', False)
    await callback.message.edit_text(
        text='Данные успешно очищены.',
        reply_markup=await gen_product_kb(user_id)
    )
