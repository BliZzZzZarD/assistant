# -*- coding: utf-8 -*-
import sys
from django.contrib import admin
from assistant.address.model import Region, City, Street, District

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


@admin.register(Region, City, Street, District)
class EstateAdmin(admin.ModelAdmin):
    save_on_top = True

