import openai
from aiogram import Dispatcher
from aiogram.utils import executor
from django.conf import settings
from django.core.management.base import BaseCommand

from tgbot_app.handlers import dp
from tgbot_app.middlewares import EmptyMiddleware
from tgbot_app.utils.set_commands import set_default_commands


async def register_middlewares(_dp):
    _dp.middleware.setup(EmptyMiddleware())


async def on_startup(_dp: Dispatcher):
    await set_default_commands(_dp)
    await register_middlewares(_dp)
    openai.api_key = settings.OPENAI_API_KEY


class Command(BaseCommand):
    def handle(self, *args, **options):
        executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)
