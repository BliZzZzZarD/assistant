# -*- coding: utf-8 -*-
from django.apps import AppConfig

import sys

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


class ManagerAppConfig(AppConfig):
    name = "assistant.manager"
    verbose_name = "Пользователи-менеджеры"
