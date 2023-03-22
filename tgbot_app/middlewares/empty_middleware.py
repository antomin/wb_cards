from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message

from tgbot_app.loader import dp


class EmptyMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: Message, cb_data: dict):
        state = dp.current_state()

        if message.text not in ('/start', '/update'):
            async with state.proxy() as data:
                if not data.state:
                    await message.delete()
                    raise CancelHandler()
