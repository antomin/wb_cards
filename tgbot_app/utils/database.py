import json

from asgiref.sync import sync_to_async
from django.conf import settings
from django.db.models import Count, ExpressionWrapper, F, IntegerField, Q

from tgbot_app.models import AppUser, Message, SeoWB, UserSession


@sync_to_async
def get_active_session(user_id):
    return UserSession.objects.filter(user=user_id, is_active=True).last()


@sync_to_async
def add_user_session(user_id, username, data):
    sessions = UserSession.objects.filter(user=user_id, is_active=True)

    if sessions:
        for session in sessions:
            session.is_active = False
            session.save()

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
        return

    session.update_field(field, value)

    if field in ('title', 'important', 'sku_plus'):
        session.is_updated = True

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
    messages = Message.objects.filter(user_session__user=user_id, is_active=True)
    for msg in messages:
        msg.is_active = False
        msg.save()


@sync_to_async
def get_last_msg(user_id):
    return Message.objects.filter(user_session__user=user_id, is_active=True).order_by('created_at').last()


@sync_to_async
def fetch_data(keywords: list | str, limit=settings.FETCH_DATA_LIMIT, sort_by='default') -> list:
    if isinstance(keywords, str):
        keywords = [word.strip() for word in keywords.split(',')]

    keyword_conditions = Q()

    for keyword in keywords:
        keyword_conditions |= Q(lemmas__contains=keyword)

    keyword_count = sum([Count("lemmas", filter=Q(lemmas__contains=keyword), distinct=True) for keyword in keywords])
    total_count = ExpressionWrapper(F("frequency") * keyword_count, output_field=IntegerField())

    queryset = SeoWB.objects.filter(keyword_conditions).annotate(
        keyword_count=keyword_count,
        total_count=total_count
    )

    if sort_by == 'total_count':
        queryset = queryset.order_by("-total_count")
    elif sort_by == 'frequency':
        queryset = queryset.order_by("-frequency", "-keyword_count")
    else:
        queryset = queryset.order_by("-keyword_count", "-frequency")

    queryset = queryset[:limit]

    return queryset
