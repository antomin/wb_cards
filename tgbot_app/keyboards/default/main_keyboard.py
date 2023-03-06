from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

main_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

main_kb.add(
    KeyboardButton('Товар'),
    KeyboardButton('Помощь'),
    KeyboardButton('Обновить'),
)
