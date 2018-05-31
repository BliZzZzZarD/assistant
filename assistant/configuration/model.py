# -*- coding: utf-8 -*-
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.db import models

import sys

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


@python_2_unicode_compatible
class Configuration(models.Model):
    site = models.CharField(_("Название сайта, до 128 символов"), max_length=128)
    phone = models.CharField(_("Телефон, до 20 символов"), max_length=20)
    email = models.EmailField(_("Email"))
    address = models.CharField(_("Адрес, до 128 символов"), max_length=128, blank=True, null=True)
    vk = models.URLField(_("Адрес вконтакте"), blank=True, null=True)
    isVk = models.BooleanField(_("Отображать ссылку вконтакте"), default=False)
    fb = models.URLField(_("Адрес facebook"), blank=True, null=True)
    isFb = models.BooleanField(_("Отображать ссылку facebook"), default=False)

    class Meta:
        verbose_name = _("Основные настройки")
        verbose_name_plural = _("Основные настройки")

    def __str__(self):
        return self.site

    def save(self, *args, **kwargs):
        self.pk = 1

        super(Configuration, self).save(*args, **kwargs)

