# -*- coding: utf-8 -*-
from django.apps import AppConfig

import sys

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


class ConfigurationAppConfig(AppConfig):
    name = "assistant.configuration"
    verbose_name = "Общие настройки"
