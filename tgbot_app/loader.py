from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from django.conf import settings

storage = MemoryStorage()
bot = Bot(token=settings.TG_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot=bot, storage=storage)
