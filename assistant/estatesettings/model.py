# -*- coding: utf-8 -*-
import sys

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


@python_2_unicode_compatible
class EstateSettingType(models.Model):
    name = models.CharField(_("Название"), max_length=255)
    description = models.TextField(_("Описание"), max_length=1024, blank=True, null=True)

    class Meta:
        ordering = ["name"]
        abstract = True

    def __str__(self):
        return self.name


class RepairType(EstateSettingType):
    class Meta:
        verbose_name = _("Тип ремонта")
        verbose_name_plural = _("Типы ремонта")


class ConstructionType(EstateSettingType):
    class Meta:
        verbose_name = _("Тип здания")
        verbose_name_plural = _("Типы здания")


class KitchenType(EstateSettingType):
    class Meta:
        verbose_name = _("Тип кухни")
        verbose_name_plural = _("Типы кухни")


class ConstructionResidenceType(EstateSettingType):
    class Meta:
        verbose_name = _("Тип частного строения")
        verbose_name_plural = _("Типы частного строения")


class WallType(EstateSettingType):
    class Meta:
        verbose_name = _("Тип стен")
        verbose_name_plural = _("Типы стен")


class OverlappingType(EstateSettingType):
    class Meta:
        verbose_name = _("Тип перекрытий")
        verbose_name_plural = _("Типы перекрытий")


class RoofType(EstateSettingType):
    class Meta:
        verbose_name = _("Тип крыши")
        verbose_name_plural = _("Типы крыши")


class GasType(EstateSettingType):
    class Meta:
        verbose_name = _("Газоснабжение")
        verbose_name_plural = _("Газоснабжение")


class WaterType(EstateSettingType):
    class Meta:
        verbose_name = _("Водоснабжение")
        verbose_name_plural = _("Водоснабжение")


class SewerageType(EstateSettingType):
    class Meta:
        verbose_name = _("Канализация")
        verbose_name_plural = _("Канализация")


class AppointmentType(EstateSettingType):
    class Meta:
        verbose_name = _("Назначение коммерческой недвижимости")
        verbose_name_plural = _("Назначения коммерческой недвижимости")


class ConstructionCommerceType(EstateSettingType):
    class Meta:
        verbose_name = _("Тип строения объекта коммерческой недвижимости")
        verbose_name_plural = _("Типы строения объекта коммерческой недвижимости")


class AppointmentLandType(EstateSettingType):
    class Meta:
        verbose_name = _("Назначение земельного участка")
        verbose_name_plural = _("Назначения земельного участка")
