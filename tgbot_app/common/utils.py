import json

import openai

from tgbot_app.common.database import (get_active_session, get_last_msg,
                                       get_msg_history, save_msg,
                                       update_field_session)
from tgbot_app.common.text_variables import (REQUEST_DESC, REQUEST_IMP,
                                             REQUEST_MAIN, REQUEST_SEO,
                                             REQUEST_STYLE)


async def get_value(user_id, field):
    session = await get_active_session(user_id)

    data = session.serializable_value(field) if session else None

    if not data or data == 'null':
        return 'Нет данных...'

    if field == 'characteristics':
        data = json.loads(data)
        result = []
        for key, value in data.items():
            result.append(f'<b>{key}</b>: <i>{value}</i>')

        return '\n'.join(result)

    return data


async def update_data(user_id, field, value):
    try:
        await update_field_session(user_id, field, value)
        return True
    except Exception:
        return False


async def get_init_text(session, add_seo):
    result = REQUEST_MAIN.format(title=session.title)

    if session.description:
        result += ' ' + REQUEST_DESC.format(desc=session.description)

    if add_seo:
        result += ' ' + REQUEST_SEO.format(seo=session.seo_plus)

    if session.important:
        result += ' ' + REQUEST_IMP.format(imp=session.important)

    if session.style:
        result += ' ' + REQUEST_STYLE.format(style=session.style)

    return result


async def gen_conversation(user_id, add_seo):
    conversation = [{'role': 'system', 'content': 'You are a helpful assistant. Fluent Russian speaks.'}]
    msg_history, msg_cnt = await get_msg_history(user_id)

    if msg_cnt == 0:
        session = await get_active_session(user_id)
        init_text = await get_init_text(session, add_seo)

        await save_msg(user_id, init_text, is_user=True)
        conversation.append({'role': 'user', 'content': init_text})

        return conversation

    async for msg in msg_history:
        conversation.append({
            'role': 'user' if msg.is_user else 'assistant',
            'content': msg.text
        })

    return conversation


async def get_chatgpt_answer(user_id, add_seo=False):
    last_msg = await get_last_msg(user_id)
    if last_msg and not last_msg.is_user:
        return last_msg.text

    conversation = await gen_conversation(user_id, add_seo)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        temperature=2,
        max_tokens=1000,
        top_p=0.9
    )

    return response['choices'][0]['message']['content']
