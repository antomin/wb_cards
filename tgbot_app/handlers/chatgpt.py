# from aiogram.dispatcher import FSMContext
# from aiogram.types import CallbackQuery, Message
#
# from tgbot_app.common.database import reset_messages, save_msg
# from tgbot_app.common.utils import get_chatgpt_answer
# from tgbot_app.keyboards.inline.chatgpt_keyboard import gen_chatgpt_kb
# from tgbot_app.keyboards.inline.product_keyboard import gen_product_kb
# from tgbot_app.loader import dp
#
#
# @dp.callback_query_handler(chatgpt_cd.filter(action='start'))
# async def chatgpt_handler(callback: CallbackQuery):
#     user_id = callback.from_user.id
#     await callback.message.edit_text('Загрузка... Может занять до 1мин...')
#
#     answer = await get_chatgpt_answer(user_id)
#     await save_msg(user_id, answer, is_user=False)
#
#     await callback.message.edit_text(text=answer, reply_markup=await gen_chatgpt_kb())
#
#
# @dp.callback_query_handler(chatgpt_cd.filter(action='specify'))
# async def specify_answer(callback: CallbackQuery, state: FSMContext):
#     await state.set_state('specify_chatgpt')
#     await callback.answer()
#     await callback.message.answer('Введите уточнения по вашему запросу:')
#
#
# @dp.message_handler(state='specify_chatgpt')
# async def set_new_msg(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     await save_msg(user_id, message.text, is_user=True)
#     await message.answer('Загрузка... Может занять до 1мин...')
#
#     answer = await get_chatgpt_answer(user_id)
#     await save_msg(user_id, answer, is_user=False)
#
#     await message.answer(text=answer, reply_markup=await gen_chatgpt_kb())
#
#     await state.reset_state()
#
#
# @dp.callback_query_handler(chatgpt_cd.filter(action='reset'))
# async def reset_chatgpt(callback: CallbackQuery):
#     user_id = callback.from_user.id
#     await reset_messages(user_id)
#
#     await callback.message.edit_text('Диалог с ChatGPT cброшен.',
#                                      reply_markup=await gen_product_kb(user_id))
