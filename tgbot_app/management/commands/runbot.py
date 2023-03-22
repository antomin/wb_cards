import openai
from aiogram.utils import executor
from django.conf import settings
from django.core.management.base import BaseCommand

from tgbot_app.common.set_commands import set_default_commands
from tgbot_app.handlers import dp
from tgbot_app.middlewares import EmptyMiddleware


async def register_middlewares(_dp):
    _dp.middleware.setup(EmptyMiddleware())


async def on_startup(_dp):
    await set_default_commands(_dp)
    await register_middlewares(_dp)
    openai.api_key = settings.OPENAI_API_KEY


class Command(BaseCommand):
    def handle(self, *args, **options):
        executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)
