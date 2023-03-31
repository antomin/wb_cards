from aiogram.dispatcher.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from tgbot_app.keyboards.inline import gen_main_kb, main_menu_cd
from tgbot_app.loader import dp
from tgbot_app.utils.text_variables import START_MSG


@dp.callback_query_handler(main_menu_cd.filter(action='main_menu'))
@dp.message_handler(CommandStart())
async def start(message: Message | CallbackQuery):
    markup = await gen_main_kb()

    if isinstance(message, CallbackQuery):
        await message.message.answer(text=START_MSG, reply_markup=markup)
        await message.answer()
    else:
        await message.answer(text=START_MSG, reply_markup=markup)
