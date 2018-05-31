# -*- coding: utf-8 -*-
import sys
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


@python_2_unicode_compatible
class Album(models.Model):
    name = models.CharField(_("Название альбома"), max_length=256)
    description = models.TextField(_("Описание"), blank=True, null=True)
    image = models.ImageField(_("Обложка альбома"), blank=True, null=True)

    class Meta:
        verbose_name = _("Альбом")
        verbose_name_plural = _("Альбомы")

    def get_picture_preview(self):
        str_html = """<a href="{src}" target="_blank"><img src="{src}" alt="{title}" style="max-width: 200px; max-height:200px;"></a>"""
        return str_html.format(src=self.image.url, title=self.name)

    get_picture_preview.allow_tags = True
    get_picture_preview.short_description = _("Обложка альбома")

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Photo(models.Model):
    album = models.ForeignKey(Album,
                              verbose_name=_("Новость"),
                              blank=True,
                              null=True)
    name = models.CharField(_("Описание фотографии"), max_length=128)
    isAlbumFace = models.BooleanField(_("Обложка альбома"), default=False)
    picture = models.ImageField(_("Фотография"),
                                upload_to='estates/images/' + now().date().__str__(),
                                blank=True,
                                null=True)

    class Meta:
        verbose_name = _("Фотография")
        verbose_name_plural = _("Фотографии")

    def get_picture_preview(self):
        str_html = """<a href="{src}" target="_blank"><img src="{src}" alt="{title}" style="max-width: 200px; max-height:200px;"></a>"""
        return str_html.format(src=self.picture.url, title=self.name)

    get_picture_preview.allow_tags = True
    get_picture_preview.short_description = _("Превью")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.isAlbumFace is True:
            try:
                album = self.album
                album.image = self.picture
                album.save()
            except Album.DoesNotExist:
                pass

            for photo in Photo.objects.filter(album=self.album):
                photo.isAlbumFace = False
                photo.save()
            self.isAlbumFace = True
        super(Photo, self).save(*args, **kwargs)
