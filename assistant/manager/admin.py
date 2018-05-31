# -*- coding: UTF-8 -*-
import sys

from django.contrib import admin

from assistant.manager.model import Manager

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


@admin.register(Manager)
class EstateAdmin(admin.ModelAdmin):
    save_on_top = True

