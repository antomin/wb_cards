from aiogram.types import CallbackQuery, Message

from tgbot_app.common.database import update_field_session
from tgbot_app.keyboards.inline.product_keyboard import gen_product_kb
from tgbot_app.keyboards.inline.update_keyboard import gen_update_kb, update_cd
from tgbot_app.loader import dp


@dp.message_handler(lambda message: 'Обновить' in message.text)
async def product_handler(message: Message):
    await message.answer(
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
