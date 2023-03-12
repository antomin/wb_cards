from aiogram.types import BotCommand


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        BotCommand('start', 'Запустить бота'),
        BotCommand('product', 'Загрузка и работа с товаром'),
        BotCommand('reset', 'Обновление товара'),
        BotCommand('help', 'Помощь по работе с ботом'),
    ])
