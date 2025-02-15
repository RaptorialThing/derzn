import re
from django.shortcuts import render
from .models import HelpPage, CategoryHelp


def help(request, category=None):
    nodes = CategoryHelp.objects.filter(is_published=True)
    if category is not None:
        context = HelpPage.objects.filter(category__url_tag="/" + category, category__is_published=True).first()
        if context:
            return render(request, "help/help.html", {"context": context, "nodes": nodes})
    url_redirect = request.META.get('HTTP_REFERER')
    try:
        url_tag = re.search(r"(?<=drevo)/\w+|/$", url_redirect).group(0)
        context = HelpPage.objects.filter(category__url_tag=url_tag, category__is_published=True).first()
        if context:
            return render(request, "help/help.html", {"context": context, "nodes": nodes})
    except AttributeError:
        context = HelpPage.objects.filter(category__url_tag='/', category__is_published=True).first()
        return render(request, "help/help.html", {"context": context, "nodes": nodes})
    except Exception:
        return render(request, "help/help_404.html", {'nodes': nodes})
    return render(request, "help/help_404.html", {'nodes': nodes})