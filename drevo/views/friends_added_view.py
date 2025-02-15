import datetime

from django.shortcuts import render

from ..models import FriendsTerm
from ..models import FriendsInviteTerm
from users.models import Profile, User


def friends_added_view(request):
    """
    Контрол страницы "Добавить в друзья"
    """
    context = {'profiles': []}
    first_name_predicate = request.GET.get('first')
    last_name_predicate = request.GET.get('last')

    # Добавление в друзья
    if request.GET.get('add'):
        _add_friend(request.user.id, request.GET.get('add'))

    exclude_ids = [request.user.id]
    profiles = Profile.objects.exclude(id__in=exclude_ids)
    for profile in profiles:
        data = {}
        if first_name_predicate and not last_name_predicate:
            user = User.objects.filter(id=profile.user_id, first_name__contains=first_name_predicate).first()
        elif not first_name_predicate and last_name_predicate:
            user = User.objects.filter(id=profile.user_id, last_name__contains=last_name_predicate).first()
        elif first_name_predicate and last_name_predicate:
            user = User.objects.filter(id=profile.user_id, first_name__contains=first_name_predicate,
                                       last_name__contains=last_name_predicate).first()
        else:
            user = User.objects.filter(id=profile.user_id).first()
        if not user:
            continue
        if not user.first_name or not user.last_name:
            continue

        data['first_name'] = user.first_name
        data['last_name'] = user.last_name
        data['avatar'] = profile.avatar or ''
        data['user_id'] = profile.user_id
        data['relation_to_request_user'] = 'no_relation'
    
        if FriendsInviteTerm.objects.filter(sender=request.user.id, recipient = profile.user_id).exists():
            data['relation_to_request_user'] = 'subscriber'
        elif FriendsTerm.objects.filter(user = request.user.id, friend = profile.user_id).exists():
            data['relation_to_request_user'] = 'friend'
        context['profiles'].append(data)

    template_name = 'drevo/friends_added.html'
    return render(request, template_name, context)


def _add_friend(user_id: int, friend_id: str) -> None:
    """
    Отправить заявку на дружбу
    """
    try:
        term = FriendsInviteTerm.objects.get(sender_id = user_id, recipient_id = int(friend_id))
    except:
        try:
            friendship = FriendsTerm.objects.get(user = user_id, friend = int(friend_id))
        except:
            if not user_id == int(friend_id):
                FriendsInviteTerm.objects.create(sender_id=user_id, recipient_id=int(friend_id))
            else:
                pass
