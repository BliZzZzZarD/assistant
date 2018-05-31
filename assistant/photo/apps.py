# -*- coding: utf-8 -*-
import sys
from django.apps import AppConfig

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


class PhotoAppConfig(AppConfig):
    name = "assistant.photo"
    verbose_name = "Фотоматериалы"
