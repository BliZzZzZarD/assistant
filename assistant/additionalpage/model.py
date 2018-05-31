# -*- coding: utf-8 -*-
import sys

from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


@python_2_unicode_compatible
class AdditionalPage(models.Model):
    name = models.CharField(_("Название страницы"), max_length=255)
    slug = models.SlugField(_("URL страницы"), max_length=255, unique=True)
    isShowNavigation = models.BooleanField(_("Отображать в панели навигации"), default=False)
    textPage = RichTextUploadingField(_("Содержание страницы"), default="")
    picture = models.FileField(_("Логотип страницы 200x200"),
                                           upload_to='pages/images/',
                                           blank=True,
                                           null=True)

    def get_picture_preview(self):
        str_html = """<a href="{src}" target="_blank"><img src="{src}" alt="preview Photo" style="max-width: 200px; max-height:200px;"></a>"""
        return str_html.format(src=self.picture.url)

    get_picture_preview.allow_tags = True
    get_picture_preview.short_description = _("Превью")

    class Meta:
        verbose_name = _("Дополнительная страница")
        verbose_name_plural = _("Дополнительные страницы")

    def __str__(self):
        return self.name
