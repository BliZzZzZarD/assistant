# -*- coding: utf-8 -*-
import sys

from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


@python_2_unicode_compatible
class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(_("Имя"), max_length=128)
    surname = models.CharField(_("Фамилия"), max_length=128, blank=True)
    phone = models.CharField(_("Телефон"), max_length=11, blank=True)

    class Meta:
        verbose_name = _("Менеджер")
        verbose_name_plural = _("Менеджеры")

    def __str__(self):
        return self.name + ' ' + self.surname

