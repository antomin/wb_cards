from aiogram import Bot, Dispatcher
from django.conf import settings

bot = Bot(token=settings.TG_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot=bot)
