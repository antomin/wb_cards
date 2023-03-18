from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from tgbot_app.common.media import HEADER_PHOTO_ID
from tgbot_app.common.text_variables import START_MSG
from tgbot_app.keyboards.inline.start_keyboard import gen_main_kb
from tgbot_app.loader import dp


@dp.message_handler(CommandStart())
async def start(message: Message):
    markup = await gen_main_kb()
    await message.delete()
    await message.answer_photo(photo=HEADER_PHOTO_ID, caption=START_MSG, reply_markup=markup)
