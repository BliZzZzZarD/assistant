# -*- coding: utf-8 -*-
import sys
from django.contrib import admin
from assistant.additionalpage.model import AdditionalPage

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


@admin.register(AdditionalPage)
class ServiceAdmin(admin.ModelAdmin):
    save_on_top = True
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ["get_picture_preview"]
