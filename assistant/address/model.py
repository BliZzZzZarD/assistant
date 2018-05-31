# -*- coding: utf-8 -*-
import sys

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


@python_2_unicode_compatible
class Region(models.Model):
    name = models.CharField(_("Название региона"), max_length=128)

    class Meta:
        ordering = ['name']
        verbose_name = _("Регион")
        verbose_name_plural = _("Регионы")

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class City(models.Model):
    name = models.CharField(_("Название населенного пункта"), max_length=128)
    region = models.ForeignKey(Region, verbose_name=_("Регион"))
    isCityWithDistrict = models.BooleanField(_("Населенный пункт с районами"), default=False)

    class Meta:
        ordering = ['name']
        verbose_name = _("Населенный пункт")
        verbose_name_plural = _("Населенные пункты")

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class District(models.Model):
    name = models.CharField(_("Название района"), max_length=128)
    region = models.ForeignKey(City, verbose_name=_("Город"))

    class Meta:
        ordering = ['name']
        verbose_name = _("Район")
        verbose_name_plural = _("Районы")

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Street(models.Model):
    ordering = ['name']
    name = models.CharField(_("Название улицы"), max_length=128)
    city = models.ForeignKey(City, verbose_name=_("Город"))
    district = models.ForeignKey(District, verbose_name=_("Район"), blank=True, null=True)

    class Meta:
        verbose_name = _("Улица")
        verbose_name_plural = _("Улицы")

    def __str__(self):
        return self.name

