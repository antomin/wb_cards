import openai

from tgbot_app.utils.database import (get_active_session, get_last_msg,
                                      get_msg_history, save_msg)
from tgbot_app.utils.text_variables import (REQUEST_FINAL, REQUEST_IMP,
                                            REQUEST_MAIN, REQUEST_MINUS,
                                            REQUEST_SEO, REQUEST_SEO_PHR,
                                            REQUEST_TITLE)


async def get_init_text(session):
    result = REQUEST_MAIN.format(style=session.style)

    if session.title:
        result += '\n' + REQUEST_TITLE.format(title=session.title)
    if session.important:
        result += '\n' + REQUEST_IMP.format(important=session.important)
    if session.seo_dict:
        result += '\n' + REQUEST_SEO.format(seo_dict=session.seo_dict)
    if session.seo_phrases:
        result += '\n' + REQUEST_SEO_PHR.format(seo_phrases=session.seo_phrases)
    if session.minus_words:
        result += '\n' + REQUEST_MINUS.format(minus_keywords=session.minus_words)

    result += '\n' + REQUEST_FINAL

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
    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo",
        messages=conversation,
        temperature=2,
        max_tokens=1000,
        top_p=0.9,
        timeout=60,
    )

    return response['choices'][0]['message']['content']
