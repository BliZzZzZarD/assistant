# -*- coding: UTF-8 -*-
import sys

from django.contrib import admin

from assistant.marketing.model import Partner, PartnerType, PartnerProgram, BannerVertical, BannerHorizontal

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


@admin.register(PartnerType)
class PartnerTypeAdmin(admin.ModelAdmin):
    save_on_top = True


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    save_on_top = True
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['get_picture_preview', 'get_banner_vertical_preview', 'get_banner_horizontal_preview']
    fieldsets = (
        (None, {
            'fields': ('name', 'type', 'slug', 'url', 'isShowInMainPage')
        }),
        ('Логотип', {
            'fields': ('picture', 'get_picture_preview')
        }),
        ('Рекламные баннеры', {
            'fields': ('advertBannerVertical', 'get_banner_vertical_preview', 'advertBannerHorizontal',
                       'get_banner_horizontal_preview', ('isShowBannerVertical', 'isShowBannerHorizontal'))
        }),
        ('Описание', {
            'fields': ('textPage',)
        }),
        ('Альбом', {
            'fields': ('album',)
        })
    )


@admin.register(BannerVertical, BannerHorizontal)
class PartnerAdmin(admin.ModelAdmin):
    save_on_top = True
    readonly_fields = ['get_picture_preview']


@admin.register(PartnerProgram)
class PartnerProgramAdmin(admin.ModelAdmin):
    save_on_top = True
    prepopulated_fields = {'slug': ('name',)}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "partner":
            kwargs["queryset"] = Partner.objects.filter(type__name="Банк")
        return super(PartnerProgramAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
