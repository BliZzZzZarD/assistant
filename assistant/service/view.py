# -*- coding: utf-8 -*-
import sys

from django.shortcuts import render

from assistant.service.tools import get_all_service_context, get_service_context

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


def show_all_service(request):
    context = get_all_service_context()
    return render(request, 'service/allService.html', context)


def show_service(request, service_slug):
    context = get_service_context(service_slug)
    return render(request, 'service/service.html', context)
