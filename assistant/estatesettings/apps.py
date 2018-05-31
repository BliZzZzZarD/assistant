# -*- coding: utf-8 -*-
from django.apps import AppConfig

import sys

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


class EstateSettingAppConfig(AppConfig):
    name = "assistant.estatesettings"
    verbose_name = "Настройки недвижимости"
