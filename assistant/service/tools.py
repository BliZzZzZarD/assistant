# -*- coding: utf-8 -*-
import sys
from assistant.service.model import Service

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


def get_service_main_page():
    return Service.objects.filter(isShow=True, isShowMainPage=True)


def get_all_service_context():
    services = Service.objects.filter(isShow=True)

    context = {
        'services': services,
    }

    return context


def get_service_context(service_slug):
    service = Service.objects.get(slug=service_slug)

    context = {
        'service': service,
    }

    return context
