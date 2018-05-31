# -*- coding: utf-8 -*-
import sys
from django.contrib import admin

from assistant.photo.models import Photo, Album

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


class PhotoInline(admin.StackedInline):
    model = Photo
    extra = 0
    fields = ["name", "picture", "get_picture_preview", "isAlbumFace"]
    readonly_fields = ["get_picture_preview"]


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    save_on_top = True
    inlines = [
        PhotoInline,
    ]
    fields = ["name", "description", "get_picture_preview"]
    readonly_fields = ["get_picture_preview"]
