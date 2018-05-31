# -*- coding: utf-8 -*-
from django.apps import AppConfig

import sys

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


class MarketingAppConfig(AppConfig):
    name = "assistant.marketing"
    verbose_name = "Маркетинг"
