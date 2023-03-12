from aiogram.types import Message

from tgbot_app.loader import dp


@dp.message_handler(commands=['help'])
async def product_handler(message: Message):
    await message.answer('Помощь ла-ла-ла!!!')
