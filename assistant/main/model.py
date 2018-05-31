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
class Slide(models.Model):
    name = models.CharField(_("Название слайда, до 28 символов"), max_length=28)

    class Meta:
        verbose_name = _("Слайд для карусели на главной странице")
        verbose_name_plural = _("Слайды для карусели на главной странице")

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Saying(models.Model):
    signature = models.CharField(_("Подпись, до 128 символов"), max_length=128)
    note = models.TextField(_("Заметка, до 500 символов"), max_length=500, default="")
    isShow = models.BooleanField(_("Отображать на главной странице"), default=False)

    class Meta:
        ordering = ['isShow']
        verbose_name = _("Заметка на главной странице")
        verbose_name_plural = _("Заметка на главной странице")

    def __str__(self):
        return self.signature

    def save(self, *args, **kwargs):
        if self.isShow:
            saying = Saying.objects.all()
            for say in saying:
                say.isShow = False
                say.save()

        super(Saying, self).save(*args, **kwargs)


@python_2_unicode_compatible
class AdditionalInfo(models.Model):
    textPage = RichTextUploadingField(_("Дополнительная информация для главной страницы"))

    class Meta:
        verbose_name = _("Блок информации для главной страницы")
        verbose_name_plural = _("Блок информации для главной страницы")

    def __str__(self):
        return "Редактировать блок"

    def save(self, *args, **kwargs):
        if AdditionalInfo.objects.get(pk=1) is not None:
            self.pk = 1

        super(AdditionalInfo, self).save(*args, **kwargs)

