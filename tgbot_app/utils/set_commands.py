from aiogram import Dispatcher
from aiogram.types import BotCommand


async def set_default_commands(dp: Dispatcher):
    await dp.bot.delete_my_commands()
    await dp.bot.set_my_commands([
        BotCommand('start', 'Главное меню'),
        BotCommand('reset', 'Обновление товара')
    ])
