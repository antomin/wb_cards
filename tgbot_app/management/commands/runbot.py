from aiogram.utils import executor
from django.core.management.base import BaseCommand

from tgbot_app.handlers import dp


class Command(BaseCommand):
    def handle(self, *args, **options):
        executor.start_polling(dispatcher=dp, skip_updates=True)
