# -*- coding: utf-8 -*-
import sys
from assistant.additionalpage.model import AdditionalPage

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


def get_pages_navigation_context():
    pages = AdditionalPage.objects.filter(isShowNavigation=True)[:4]

    context = {
        'pages': pages,
    }

    return context


def get_page_context(page_slug):
    page = AdditionalPage.objects.get(slug=page_slug)

    context = {
        'page': page,
    }

    return context
