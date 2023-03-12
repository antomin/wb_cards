from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from tgbot_app.loader import dp


@dp.message_handler(CommandStart())
async def start(message: Message):
    await message.answer(text='Start handler')
