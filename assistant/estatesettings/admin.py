# -*- coding: utf-8 -*-
import sys
from django.contrib import admin

from assistant.estatesettings.model import RepairType, ConstructionType, KitchenType, ConstructionResidenceType, \
    SewerageType, WaterType, GasType, RoofType, OverlappingType, WallType, AppointmentType, ConstructionCommerceType, \
    AppointmentLandType

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


@admin.register(RepairType, ConstructionType, KitchenType, ConstructionResidenceType, SewerageType, WaterType,
                GasType, RoofType, OverlappingType, WallType, AppointmentType, ConstructionCommerceType,
                AppointmentLandType)
class EstateAdmin(admin.ModelAdmin):
    save_on_top = True

