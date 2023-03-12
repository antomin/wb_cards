import json

import openai

from tgbot_app.common.database import (get_active_session, get_last_msg,
                                       get_msg_history, save_msg,
                                       update_field_session)
from tgbot_app.common.wb_parser import parse_wb


async def get_value(user_id, field):
    session = await get_active_session(user_id)

    if field == 'other_descriptions':
        data = [session.other_descriptions_1, session.other_descriptions_2, session.other_descriptions_3]
        result = []

        for desc in data:
            if desc:
                result.append(desc)

        return '\n\n'.join(result) if result else 'Нет данных...'

    data = session.serializable_value(field)

    if not data:
        return 'Нет данных...'

    if field == 'product_characteristics':
        data = json.loads(data)
        result = []
        for key, value in data.items():
            result.append(f'<b>{key}</b>: <i>{value}</i>')

        return '\n'.join(result)

    return data


async def update_data(user_id, field, value):
    try:
        if field == 'product_characteristics':
            result = {}
            data = value.split('\n')

            for char in data:
                key, value = [i.strip() for i in char.split(':')[:2]]
                result[key] = value

            result_json = json.dumps(result, ensure_ascii=False)

            await update_field_session(user_id, field, result_json)

            return True

        if field == 'other_descriptions':
            data = value.split()

            for idx in range(1, 4):
                db_field = field + '_' + str(idx)
                await update_field_session(user_id, db_field, None)

            for idx, scu in enumerate(data[:3], start=1):
                scu = scu.strip()
                parse_data = await parse_wb(scu)
                description = parse_data.get('description')

                if description:
                    db_field = field + '_' + str(idx)
                    await update_field_session(user_id, db_field, description)

            return True

        await update_field_session(user_id, field, value)

        return True

    except Exception:
        return False


async def gen_conversation(user_id):
    conversation = [{'role': 'system', 'content': 'You are a helpful assistant. Fluent Russian speaks.'}]
    msg_history, msg_cnt = await get_msg_history(user_id)

    if msg_cnt == 0:
        session = await get_active_session(user_id)
        init_text = f'Напиши описание товара для маркетплейса, используя следующую информацию. Название торговой' \
                    f'марки {session.product_title}.'
        await save_msg(user_id, init_text, is_user=True)
        conversation.append({'role': 'user', 'content': init_text})

        return conversation

    async for msg in msg_history:
        conversation.append({
            'role': 'user' if msg.is_user else 'assistant',
            'content': msg.text
        })

    return conversation


async def get_chatgpt_answer(user_id):
    last_msg = await get_last_msg(user_id)
    if last_msg and not last_msg.is_user:
        return last_msg.text

    conversation = await gen_conversation(user_id)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        temperature=2,
        max_tokens=1000,
        top_p=0.9
    )

    return response['choices'][0]['message']['content']
