# -*- coding: utf-8 -*-
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

import sys

from assistant.photo.models import Album

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


@python_2_unicode_compatible
class PartnerType(models.Model):
    name = models.CharField(_("Название"), max_length=128)
    # -*- описание -*-
    description = models.TextField(_("Описание"), blank=True, null=True, max_length=2048)

    class Meta:
        ordering = ["name"]
        verbose_name = "Тип партнер"
        verbose_name_plural = "Типы партнеров"

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Partner(models.Model):
    name = models.CharField(_("Название"), max_length=128)
    type = models.ForeignKey(PartnerType, verbose_name="тип партнера")
    slug = models.SlugField(_("URL объекта"), max_length=255, unique=True)
    url = models.URLField(_("URL сайта партнера"), blank=True, null=True)
    picture = models.ImageField(_("Логотип(рекомендуемый соотношение сторон 1:1)"),
                                upload_to='partners/images/',
                                blank=True,
                                null=True)
    isShowInMainPage = models.BooleanField(_("Показ на главной странице"), default=False)
    # -*- рекламные баннеры -*-
    advertBannerVertical = models.ImageField(_("Рекламный баннер вертикальный (размер 250X500px)"),
                                             upload_to='partners/images/',
                                             blank=True,
                                             null=True)
    advertBannerHorizontal = models.ImageField(_("Рекламный баннер горизонтальный (размер 1000X100px)"),
                                               upload_to='partners/images/',
                                               blank=True,
                                               null=True)
    # -*- фотоматериалы -*-
    album = models.ForeignKey(Album, verbose_name="Сертификаты и благодарности", blank=True, null=True)
    isShowBannerVertical = models.BooleanField(_("Отображать вертикальный баннер"), default=False)
    isShowBannerHorizontal = models.BooleanField(_("Отображать горизонтальный баннер"), default=False)
    # -*- описание -*-
    textPage = RichTextUploadingField(_("Описание, максимум 2000 символа"),
                                      blank=True,
                                      null=True,
                                      max_length=2000)

    def get_picture_preview(self):
        str_html = """<a href="{src}" target="_blank"><img src="{src}" alt="preview Photo" style="max-width: 200px; 
        max-height:200px;"></a> """
        return str_html.format(src=self.picture.url)

    def get_banner_vertical_preview(self):
        str_html = """<a href="{src}" target="_blank"><img src="{src}" alt="preview Photo" style="max-width: 200px; 
        max-height:200px;"></a> """
        return str_html.format(src=self.advertBannerVertical.url)

    def get_banner_horizontal_preview(self):
        str_html = """<a href="{src}" target="_blank"><img src="{src}" alt="preview Photo" style="max-width: 200px; 
        max-height:200px;"></a> """
        return str_html.format(src=self.advertBannerHorizontal.url)

    get_picture_preview.allow_tags = True
    get_picture_preview.short_description = _("Превью")

    get_banner_vertical_preview.allow_tags = True
    get_banner_vertical_preview.short_description = _("Превью")

    get_banner_horizontal_preview.allow_tags = True
    get_banner_horizontal_preview.short_description = _("Превью")

    class Meta:
        ordering = ["name"]
        verbose_name = "Партнер"
        verbose_name_plural = "Партнеры"

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class PartnerProgram(models.Model):
    partner = models.ForeignKey(Partner, verbose_name="Партнер")
    name = models.CharField(_("Название программы"), max_length=128)
    slug = models.SlugField(_("URL объекта"), max_length=255, unique=True)
    term = models.IntegerField(_("Максимальный срок кредитования, лет"))
    rate = models.FloatField(_("Процентная ставка, % годовых"))
    # -*- описание -*-
    description = RichTextUploadingField(_("Описание, максимум 2000 символа"),
                                         blank=True,
                                         null=True,
                                         max_length=2000)

    class Meta:
        ordering = ["name"]
        verbose_name = "Партнерская программа"
        verbose_name_plural = "Партнерские программы"

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class BannerHorizontal(models.Model):
    name = models.CharField(_("Название"), max_length=128)
    picture = models.ImageField(_("Рекламный баннер горизонтальный (размер 1000X100px)"),
                                upload_to='banner-horizontal/')
    isShow = models.BooleanField(_("Отображать в рекламных блоках"), default=False)

    def get_picture_preview(self):
        str_html = """<a href="{src}" target="_blank"><img src="{src}" alt="preview Photo" style="max-width: 200px; 
        max-height:200px;"></a> """
        return str_html.format(src=self.picture.url)

    get_picture_preview.allow_tags = True
    get_picture_preview.short_description = _("Превью")

    class Meta:
        ordering = ["name"]
        verbose_name = "Горизонтальный баннер"
        verbose_name_plural = "Горизонтальные баннеры"

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class BannerVertical(models.Model):
    name = models.CharField(_("Название"), max_length=128)
    picture = models.ImageField(_("Рекламный баннер вертикальный (размер 250X500px)"),
                                upload_to='banner-horizontal/')
    isShow = models.BooleanField(_("Отображать в рекламных блоках"), default=False)

    def get_picture_preview(self):
        str_html = """<a href="{src}" target="_blank"><img src="{src}" alt="preview Photo" style="max-width: 200px; 
        max-height:200px;"></a> """
        return str_html.format(src=self.picture.url)

    get_picture_preview.allow_tags = True
    get_picture_preview.short_description = _("Превью")

    class Meta:
        ordering = ["name"]
        verbose_name = "Вертикальный баннер"
        verbose_name_plural = "Вертикальные баннеры"

    def __str__(self):
        return self.name
