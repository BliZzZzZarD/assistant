# -*- coding: utf-8 -*-
import sys

from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder

from assistant.configuration.model import Configuration
from assistant.main.model import Slide, Saying, AdditionalInfo
from assistant.marketing.model import Partner
from assistant.marketing.tools import get_best_rate
from assistant.service.tools import get_service_main_page

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


def get_main_context():
    services = get_service_main_page()
    saying = get_saying()
    slides = get_slides()
    partners = get_partners()
    add_info = get_add_info()

    context = {
        'services': services,
        'slides': slides,
        'saying': saying,
        'partners': partners,
        'add_info': add_info,
    }

    return context


def get_slides():
    return Slide.objects.all()


def get_saying():
    try:
        saying = Saying.objects.get(isShow=True)
    except Saying.DoesNotExist:
        saying = None

    return saying


def get_configuration():
    return serialize('json', Configuration.objects.all())


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Configuration):
            return str(obj)
        return super().default(obj)


def get_partners():
    return Partner.objects.filter(isShowInMainPage=True)


def get_add_info():
    try:
        add_info = AdditionalInfo.objects.get(pk=1)
    except AdditionalInfo.DoesNotExist:
        add_info = None

    return add_info


def get_contact_context():
    try:
        configuration = Configuration.objects.last()
    except Configuration.DoesNotExist:
        configuration = {}

    return {'configuration': configuration}


def get_calculator_context(cost):
    if cost is not None:
        rate = get_best_rate()
    else:
        rate = None

    return {
        'cost': cost.replace('%', '.'),
        'rate': str(rate).replace(',', '.')
    }

