# -*- coding: utf-8 -*-
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.db import models

import sys

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


@python_2_unicode_compatible
class Service(models.Model):
    name = models.CharField(_("Название услуги"), max_length=255)
    shortDescription = models.TextField(_("Краткое описание услуги"), max_length=255, default="")
    slug = models.SlugField(_("URL новости"), max_length=255, unique=True)
    isShow = models.BooleanField(_("Отображать услугу"), default=False)
    isShowMainPage = models.BooleanField(_("Отображать услугу на главной странице"), default=False)
    textPage = RichTextUploadingField(_("Страница услуги"), default="")

    class Meta:
        verbose_name = _("Услуга")
        verbose_name_plural = _("Услуги")

    def __str__(self):
        return self.name
