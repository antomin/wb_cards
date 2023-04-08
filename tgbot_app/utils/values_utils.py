import json

from tgbot_app.utils.database import get_active_session, update_field_session
from tgbot_app.utils.wb_parser import parse_wb


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


async def get_raw_text(scu_list: list) -> str:
    raw_text = ''

    for scu in scu_list:
        if scu.isdigit():
            data = await parse_wb(scu)
            if data:
                if data.get('title'):
                    raw_text += data.get('title') + ' '
                if data.get('description'):
                    raw_text += data.get('description') + ' '

    return raw_text
