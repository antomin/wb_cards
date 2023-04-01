import openai

from tgbot_app.utils.database import (get_active_session, get_last_msg,
                                      get_msg_history, save_msg)
from tgbot_app.utils.text_variables import (REQUEST_DESC, REQUEST_IMP,
                                            REQUEST_MAIN, REQUEST_MIN,
                                            REQUEST_PHR, REQUEST_SEO,
                                            REQUEST_STYLE)


async def get_init_text(session):
    result = ''

    if session.title:
        result += REQUEST_MAIN.format(title=session.title)
    if session.description:
        result += ' ' + REQUEST_DESC.format(desc=session.description)
    if session.seo_dict:
        _seo = ''
        if session.seo_dict:
            _seo += session.seo_dict
        if session.keywords:
            _seo += ' ' + session.keywords
        result += ' ' + REQUEST_SEO.format(seo=_seo)
    if session.seo_phrases:
        result += ' ' + REQUEST_PHR.format(phr=session.seo_phrases)
    if session.minus_words:
        result += ' ' + REQUEST_MIN.format(min=session.minus_words)
    if session.important:
        result += ' ' + REQUEST_IMP.format(imp=session.important)
    if session.style and session.style != 'обычный':
        result += ' ' + REQUEST_STYLE.format(style=session.style)

    return result


async def gen_conversation(user_id):
    conversation = [{'role': 'system', 'content': 'You are a helpful assistant. Fluent Russian speaks.'}]
    msg_history, msg_cnt = await get_msg_history(user_id)

    if msg_cnt == 0:
        session = await get_active_session(user_id)
        init_text = await get_init_text(session)

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