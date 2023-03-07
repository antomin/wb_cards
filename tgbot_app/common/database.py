import json

from asgiref.sync import sync_to_async

from tgbot_app.models import AppUser, UserSession


@sync_to_async
def get_active_session(user_id):
    return UserSession.objects.filter(user=user_id, is_active=True).first()


@sync_to_async
def add_user_session(from_user, data):
    user = AppUser.objects.get(id=int(from_user.id))

    if not user:
        user = AppUser(id=int(from_user.id), username=from_user.username)
        user.save()

    session = UserSession(
        user=user,
        product_title=data.get('title'),
        product_description=data.get('description'),
        product_characteristics=json.dumps(data.get('characteristics'), ensure_ascii=False),
    )
    session.save()
