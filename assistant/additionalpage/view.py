# -*- coding: utf-8 -*-
from django.shortcuts import render

from assistant.additionalpage.tools import get_page_context

import sys

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


def page(request, page_slug):
    context = get_page_context(page_slug)
    return render(request, 'page.html', context)
