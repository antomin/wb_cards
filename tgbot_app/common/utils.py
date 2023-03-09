import json

from tgbot_app.common.database import get_active_session, update_field_session
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
