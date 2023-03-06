from aiogram.types import Message

from tgbot_app.loader import dp


@dp.message_handler(lambda message: 'Помощь' in message.text)
async def product_handler(message: Message):
    await message.answer('Помощь ла-ла-ла!!!')
