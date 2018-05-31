# -*- coding: utf-8 -*-
from django.apps import AppConfig

import sys

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


class AdditionalPageAppConfig(AppConfig):
    name = "assistant.additionalpage"
    verbose_name = "Дополнительно"
