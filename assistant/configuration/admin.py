# -*- coding: utf-8 -*-
import sys
from django.contrib import admin

from assistant.configuration.model import Configuration

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


@admin.register(Configuration)
class ConfigurationAdmin(admin.ModelAdmin):
    pass
