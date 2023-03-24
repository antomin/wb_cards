from aiogram import Dispatcher


async def set_default_commands(dp: Dispatcher):
    await dp.bot.delete_my_commands()
