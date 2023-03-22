from aiogram.dispatcher.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from tgbot_app.common.text_variables import START_MSG
from tgbot_app.keyboards.inline import gen_main_kb, main_menu_cd
from tgbot_app.loader import dp


@dp.callback_query_handler(main_menu_cd.filter(action='main_menu'))
@dp.message_handler(CommandStart())
async def start(message: Message | CallbackQuery):
    markup = await gen_main_kb()

    if isinstance(message, CallbackQuery):
        await message.message.edit_text(text=START_MSG, reply_markup=markup)
    else:
        await message.answer(text=START_MSG, reply_markup=markup)
