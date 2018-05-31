# -*- coding: UTF-8 -*-
import sys
from django.contrib import admin

from assistant.main.model import Slide, Saying, AdditionalInfo

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


@admin.register(Slide, Saying, AdditionalInfo)
class ServiceAdmin(admin.ModelAdmin):
    pass
