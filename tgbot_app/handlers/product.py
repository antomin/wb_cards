from aiogram.types import Message

from tgbot_app.loader import dp


@dp.message_handler(lambda message: 'Товар' in message.text)
async def product_handler(message: Message):
    await message.answer('Товар........')
