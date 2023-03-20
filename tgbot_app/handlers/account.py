from aiogram.types import CallbackQuery, Message

from tgbot_app.keyboards.inline import main_menu_cd
from tgbot_app.loader import dp


@dp.callback_query_handler(main_menu_cd.filter(action='account'))
async def account(callback: CallbackQuery):
    await callback.answer(text='Раздел на доработке.', show_alert=True)
