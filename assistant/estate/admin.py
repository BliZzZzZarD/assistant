# -*- coding: utf-8 -*-
import sys

from django.contrib import admin
from django.db import models
from django.forms import TextInput, NumberInput

from assistant.estate.model import ApartmentEstate, ResidenceEstate, CommerceEstate, LandEstate
from assistant.django_google_maps import widgets as map_widgets
from assistant.django_google_maps import fields as map_fields

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


@admin.register(ApartmentEstate)
class ApartmentEstateAdmin(admin.ModelAdmin):
    readonly_fields = ['caption', ]
    save_on_top = True
    list_display = ['article', 'name', 'address']
    prepopulated_fields = {'slug': ('article', 'name')}
    fieldsets = (
        (None, {
            'fields': ('article', 'name', 'slug', 'caption')
        }),
        ('Адрес', {
            'fields': ('region', 'city', 'street', ('number', 'literal'))
        }),
        ('Геолокация', {
            'fields': ('address', 'geolocation', 'isAutoGeo')
        }),
        ('Характеристики', {
            'fields': ('year', 'construction', ('floor', 'floors'), 'repair', ('areaCommon', 'areaLiving'), 'room'
                       , 'typeKitchen', 'height', ('new', 'isRoom', 'isStudio', 'isPenthouse', 'wc'))
        }),
        ('Стоимость', {
            'fields': ('cost', 'costService', ('price', 'mortgagePrice', 'showCostService'))
        }),
        ('Менеджер', {
            'fields': (('manager', 'showManager'),)
        }),
        ('Описание', {
            'fields': ('shortDescription', 'description',)
        }),
        ('Фотоматериалы', {
            'fields': ('album',)
        }),
    )
    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget(attrs={'data-map-type': 'roadmap'})},
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.IntegerField: {'widget': NumberInput(attrs={'size': '20'})},
        models.FloatField: {'widget': NumberInput(attrs={'size': '20'})}
    }

    def get_form(self, request, obj=None, **kwargs):
        form = super(ApartmentEstateAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['name'].widget.attrs['style'] = 'width: 75%;'
        form.base_fields['slug'].widget.attrs['style'] = 'width: 75%;'
        return form


@admin.register(ResidenceEstate)
class ResidenceEstateAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['article', 'name', 'address']
    prepopulated_fields = {'slug': ('article', 'name')}
    fieldsets = (
        (None, {
            'fields': ('article', 'name', 'slug')
        }),
        ('Адрес', {
            'fields': ('region', 'city', 'street', ('number', 'literal'))
        }),
        ('Геолокация', {
            'fields': ('address', 'geolocation', 'isAutoGeo')
        }),
        ('Характеристики', {
            'fields': ('year', 'construction', 'floors', 'repair', ('areaCommon', 'areaLand'), 'distance'
                       , 'typeWall', 'typeOverlapping', 'typeRoof', 'typeGas', 'typeWater', 'typeSewerage', 'wc')
        }),
        ('Стоимость', {
            'fields': ('cost', 'costService', ('price', 'mortgagePrice', 'showCostService'))
        }),
        ('Менеджер', {
            'fields': (('manager', 'showManager'),)
        }),
        ('Описание', {
            'fields': ('shortDescription', 'description',)
        }),
        ('Фотоматериалы', {
            'fields': ('album',)
        }),
    )
    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget(attrs={'data-map-type': 'roadmap'})},
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.IntegerField: {'widget': NumberInput(attrs={'size': '20'})},
        models.FloatField: {'widget': NumberInput(attrs={'size': '20'})}
    }

    def get_form(self, request, obj=None, **kwargs):
        form = super(ResidenceEstateAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['name'].widget.attrs['style'] = 'width: 75%;'
        form.base_fields['slug'].widget.attrs['style'] = 'width: 75%;'
        return form


@admin.register(CommerceEstate)
class CommerceEstateAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['article', 'name', 'address']
    prepopulated_fields = {'slug': ('article', 'name')}
    fieldsets = (
        (None, {
            'fields': ('article', 'name', 'slug')
        }),
        ('Адрес', {
            'fields': ('region', 'city', 'street', ('number', 'literal'))
        }),
        ('Геолокация', {
            'fields': ('address', 'geolocation', 'isAutoGeo')
        }),
        ('Характеристики', {
            'fields': ('appointment', 'year', 'constructionCommerce', 'floor', 'floors', 'areaCommon')
        }),
        ('Стоимость', {
            'fields': ('cost', 'costService', ('price', 'showCostService'))
        }),
        ('Менеджер', {
            'fields': (('manager', 'showManager'),)
        }),
        ('Описание', {
            'fields': ('shortDescription', 'description',)
        }),
        ('Фотоматериалы', {
            'fields': ('album',)
        }),
    )
    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget(attrs={'data-map-type': 'roadmap'})},
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.IntegerField: {'widget': NumberInput(attrs={'size': '20'})},
        models.FloatField: {'widget': NumberInput(attrs={'size': '20'})}
    }

    def get_form(self, request, obj=None, **kwargs):
        form = super(CommerceEstateAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['name'].widget.attrs['style'] = 'width: 75%;'
        form.base_fields['slug'].widget.attrs['style'] = 'width: 75%;'
        return form


@admin.register(LandEstate)
class LandEstateAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['article', 'name', 'address']
    prepopulated_fields = {'slug': ('article', 'name')}
    fieldsets = (
        (None, {
            'fields': ('article', 'name', 'slug')
        }),
        ('Адрес', {
            'fields': ('region', 'city')
        }),
        ('Геолокация', {
            'fields': ('address', 'geolocation')
        }),
        ('Характеристики', {
            'fields': ('appointmentLand', 'areaCommon', ('isGas', 'isWater', 'isLight'))
        }),
        ('Стоимость', {
            'fields': ('cost', 'costService', 'showCostService')
        }),
        ('Менеджер', {
            'fields': (('manager', 'showManager'),)
        }),
        ('Описание', {
            'fields': ('shortDescription', 'description',)
        }),
        ('Фотоматериалы', {
            'fields': ('album',)
        }),
    )
    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget(attrs={'data-map-type': 'roadmap'})},
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.IntegerField: {'widget': NumberInput(attrs={'size': '20'})},
        models.FloatField: {'widget': NumberInput(attrs={'size': '20'})}
    }

    def get_form(self, request, obj=None, **kwargs):
        form = super(LandEstateAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['name'].widget.attrs['style'] = 'width: 75%;'
        form.base_fields['slug'].widget.attrs['style'] = 'width: 75%;'
        return form
