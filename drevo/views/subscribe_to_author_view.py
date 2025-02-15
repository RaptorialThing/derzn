from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


import json

from drevo.models import Author


@login_required
def sub_by_author(request):
    if request.method == 'GET':
        authors = Author.objects.all()
        return render(request, 'drevo/author_subscription.html', {'authors': authors})

    if request.method == 'POST':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Данные с фронта {'Война в Донбассе': True, 'Грамматика': False}
            subscribed_to_authors = json.loads(request.body)
            authors_subscribed_to = Author.objects.filter(
                name__in=subscribed_to_authors)

            for author in authors_subscribed_to:
                if subscribed_to_authors[author.name]:
                    author.subscribers.add(request.user)
                elif not subscribed_to_authors[author.name]:
                    author.subscribers.remove(request.user)

        return redirect('subscribe_to_author')
