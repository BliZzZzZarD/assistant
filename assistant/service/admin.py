# -*- coding: utf-8 -*-
import sys

from django.contrib import admin

from assistant.service.model import Service

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    save_on_top = True
    prepopulated_fields = {'slug': ('name',)}
