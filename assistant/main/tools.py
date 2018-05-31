# -*- coding: UTF-8 -*-
import sys

from assistant.service.model import Service

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


def get_service_main_page():
    return Service.objects.filter(isShow=True, isShowMainPage=True)

