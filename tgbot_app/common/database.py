import json

from asgiref.sync import sync_to_async

from tgbot_app.models import AppUser, Message, UserSession


@sync_to_async
def get_active_session(user_id):
    return UserSession.objects.filter(user=user_id, is_active=True).last()


@sync_to_async
def add_user_session(user_id, username, data):
    try:
        user = AppUser.objects.get(id=int(user_id))
    except Exception:
        user = AppUser(id=int(user_id), username=username)
        user.save()

    session = UserSession(
        user=user,
        title=data.get('title'),
        description=data.get('description'),
        characteristics=json.dumps(data.get('characteristics'), ensure_ascii=False),
    )
    session.save()


@sync_to_async
def update_field_session(user_id, field, value):

    session = UserSession.objects.filter(user=user_id, is_active=True).last()

    if not session:
        try:
            user = AppUser.objects.get(id=int(user_id))
        except Exception:
            user = AppUser(id=int(user_id))
            user.save()

        session = UserSession(user=user)

    session.update_field(field, value)
    session.save()


@sync_to_async
def save_msg(user_id, text, is_user):
    msg = Message(
        user_session=UserSession.objects.filter(user=user_id, is_active=True).last(),
        is_user=is_user,
        text=text
    )
    msg.save()


@sync_to_async
def get_msg_history(user_id):
    msg_history = Message.objects.filter(user_session__user=user_id, is_active=True).order_by('created_at')
    return msg_history, msg_history.count()


@sync_to_async
def reset_messages(user_id):
    msg_history = Message.objects.filter(user_session__user=user_id, is_active=True).order_by('created_at')
    for msg in msg_history:
        msg.is_active = False
        msg.save()


@sync_to_async
def get_last_msg(user_id):
    return Message.objects.filter(user_session__user=user_id, is_active=True).order_by('created_at').last()
