# -*- coding: utf-8 -*-
import json
import sys

import requests
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from assistant.address.model import Region, City, Street, District
from assistant.estatesettings.model import RepairType, ConstructionType, KitchenType, ConstructionResidenceType, \
    SewerageType, WaterType, GasType, RoofType, OverlappingType, WallType, AppointmentType, ConstructionCommerceType, \
    AppointmentLandType
from assistant.manager.model import Manager
from assistant.photo.models import Album
from assistant.django_google_maps import fields as map_fields
from assistant.settings import GOOGLE_MAPS_API_KEY

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


@python_2_unicode_compatible
class Estate(models.Model):
    article = models.CharField(_("Код объекта"), unique=True, max_length=255)
    name = models.CharField(_("Название объекта недвижимости"), max_length=255)
    slug = models.SlugField(_("URL объекта"), max_length=255, unique=True)
    # -*- адрес -*-
    region = models.ForeignKey(Region, verbose_name="Регион")
    city = models.ForeignKey(City, verbose_name="Город")
    district = models.ForeignKey(District, verbose_name="Район", blank=True, null=True)
    # -*- стоимость -*-
    cost = models.IntegerField(_("Стоимость"))
    costService = models.IntegerField(_("Стоимость услуг"), blank=True, null=True)
    showCostService = models.BooleanField(_("Показывать стоимость услуг"), default=False)
    # -*- менеджер -*-
    manager = models.ForeignKey(Manager, verbose_name="Менеджер", blank=True, null=True)
    showManager = models.BooleanField(_("Показывать контакты"), default=False)
    # -*- описание -*-
    shortDescription = models.TextField(_("Краткое описание (до 300 символов)"), blank=True, null=True, max_length=300)
    description = RichTextUploadingField(_("Описание"), blank=True, null=True)
    # -*- фотоматериалы -*-
    album = models.ForeignKey(Album, verbose_name="Альбом", blank=True, null=True)
    # -*- геолокация -*-
    address = map_fields.AddressField(_("Адрес"), max_length=200, blank=True, null=True)
    geolocation = map_fields.GeoLocationField(_("Координаты"), max_length=100, blank=True, null=True)

    class Meta:
        abstract = True
        ordering = ["article"]
        verbose_name = _("Объект недвижимости")
        verbose_name_plural = _("Объекты недвижимости")

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class RealEstate(Estate):
    # -*- адрес -*-
    street = models.ForeignKey(Street, verbose_name="Улица")
    number = models.IntegerField(_("Номер дома"))
    literal = models.CharField(_("Литера"), max_length=4, blank=True, null=True)
    # -*- характеристики -*-
    areaCommon = models.FloatField(_("Общая площадь, м2"))
    floors = models.IntegerField(_("Этажей в здании"))
    year = models.PositiveIntegerField(_("Год постройки"), validators=[MaxValueValidator(2050)], null=True, blank=True)
    # -*- стоимость -*-
    price = models.BooleanField(_("Указывать цену за м2"), default=False)
    # -*- геолокация -*-
    isAutoGeo = models.BooleanField(_("Определять коориднаты при сохранении"), default=False)

    class Meta:
        abstract = True
        verbose_name = _("Недвижимость (строения)")
        verbose_name_plural = _("Недвижимость (строения)")


@python_2_unicode_compatible
class PrivateEstate(RealEstate):
    # -*- характеристики -*-
    repair = models.ForeignKey(RepairType, verbose_name="Тип ремонта")
    # -*- стоимость -*-
    mortgagePrice = models.BooleanField(_("Указывать цену в ипотеку"), default=False)

    class Meta:
        abstract = True
        verbose_name = _("Недвижимость (строения)")
        verbose_name_plural = _("Недвижимость (строения)")


@python_2_unicode_compatible
class ApartmentEstate(PrivateEstate):
    # -*- характеристики -*-
    construction = models.ForeignKey(ConstructionType, verbose_name="Тип здания")
    floor = models.IntegerField(_("Этаж"), blank=True, null=True)
    areaLiving = models.FloatField(_("Жилая площадь, м2"), blank=True, null=True)
    areaKitchen = models.FloatField(_("Площадь кухни, м2"), blank=True, null=True)
    room = models.IntegerField(_("Количество комнат"))
    isStudio = models.BooleanField(_("Студия"), default=False)
    isRoom = models.BooleanField(_("Комната"), default=False)
    isPenthouse = models.BooleanField(_("Мансарда"), default=False)
    wc = models.BooleanField(_("Раздельный санузел"), default=False)
    typeKitchen = models.ForeignKey(KitchenType, verbose_name="Тип кухни", blank=True, null=True)
    height = models.FloatField(_("Высота потолков"), blank=True, null=True)
    new = models.BooleanField(_("Первичное жилье"), default=False)
    caption = models.CharField(_("Заголовок (формируется автоматически)"), max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'apartment'
        default_related_name = 'apartments'
        verbose_name = _("Квартира")
        verbose_name_plural = _("Квартиры")

    def save(self, *args, **kwargs):
        if not self.article.endswith('a'):
            self.article += 'a'

        if self.isAutoGeo:
            if self.literal is not None:
                literal = ' ' + self.literal
            else:
                literal = ''

            self.address = "Россия " + str(self.region).strip() + " " + str(self.city).strip() + " " + str(
                self.street).strip() + " " + str(self.number) + literal

            response = requests.get(url="https://maps.googleapis.com/maps/api/geocode/json?key=" + GOOGLE_MAPS_API_KEY
                                        + "&language=ru&region=ru&address=" + self.address)
            result = json.loads(response.content).get('results')[0].get('geometry').get('location')
            self.geolocation = str(result.get('lat')) + "," + str(result.get('lng'))
            self.isAutoGeo = False
        else:
            if self.address is not None:
                self.address = self.address.strip()

        if self.isRoom:
            self.caption = "Комната"
        else:
            self.caption = str(self.room) + "-комнатная"

        super(Estate, self).save(*args, **kwargs)


@python_2_unicode_compatible
class ResidenceEstate(PrivateEstate):
    # -*- характеристики -*-
    construction = models.ForeignKey(ConstructionResidenceType, verbose_name="Тип здания")
    areaLand = models.FloatField(_("Площадь участка, сот."), blank=True, null=True)
    distance = models.FloatField(_("Расстояние до центра, км"), blank=True, null=True)
    typeWall = models.ForeignKey(WallType, verbose_name="Стены", blank=True, null=True)
    typeOverlapping = models.ForeignKey(OverlappingType, verbose_name="Перекрытия", blank=True, null=True)
    typeRoof = models.ForeignKey(RoofType, verbose_name="Крыша", blank=True, null=True)
    typeGas = models.ForeignKey(GasType, verbose_name="Газоснабжение", blank=True, null=True)
    typeWater = models.ForeignKey(WaterType, verbose_name="Водоснабжение", blank=True, null=True)
    typeSewerage = models.ForeignKey(SewerageType, verbose_name="Канализация", blank=True, null=True)
    wc = models.BooleanField(_("Санузел в доме"), default=False)

    class Meta:
        db_table = 'residence'
        default_related_name = 'residences'
        verbose_name = _("Частный дом")
        verbose_name_plural = _("Частные дома")

    def save(self, *args, **kwargs):
        if not self.article.endswith('r'):
            self.article += 'r'

        if self.isAutoGeo:
            if self.literal is not None:
                literal = ' ' + self.literal
            else:
                literal = ''

            self.address = "Россия " + str(self.region).strip() + " " + str(self.city).strip() + " " + str(
                self.street).strip() + " " + str(self.number) + literal

            response = requests.get(url="https://maps.googleapis.com/maps/api/geocode/json?key=" + GOOGLE_MAPS_API_KEY
                                        + "&language=ru&region=ru&address=" + self.address)
            result = json.loads(response.content).get('results')[0].get('geometry').get('location')
            self.geolocation = str(result.get('lat')) + "," + str(result.get('lng'))
            self.isAutoGeo = False
        else:
            if self.address is not None:
                self.address = self.address.strip()

        super(Estate, self).save(*args, **kwargs)


@python_2_unicode_compatible
class CommerceEstate(RealEstate):
    # -*- характеристики -*-
    appointment = models.ForeignKey(AppointmentType, verbose_name="Назначение")
    floor = models.IntegerField(_("Этаж"), blank=True, null=True)
    constructionCommerce = models.ForeignKey(ConstructionCommerceType, verbose_name="Тип здания", blank=True, null=True)

    class Meta:
        db_table = 'commerce'
        default_related_name = 'commerces'
        verbose_name = _("Коммерческая недвижимость")
        verbose_name_plural = _("Коммерческая недвижимость")

    def save(self, *args, **kwargs):
        if not self.article.endswith('c'):
            self.article += 'c'

        if self.isAutoGeo:
            if self.literal is not None:
                literal = ' ' + self.literal
            else:
                literal = ''

            self.address = "Россия " + str(self.region).strip() + " " + str(self.city).strip() + " " + str(
                self.street).strip() + " " + str(self.number) + literal

            response = requests.get(url="https://maps.googleapis.com/maps/api/geocode/json?key=" + GOOGLE_MAPS_API_KEY
                                        + "&language=ru&region=ru&address=" + self.address)
            result = json.loads(response.content).get('results')[0].get('geometry').get('location')
            self.geolocation = str(result.get('lat')) + "," + str(result.get('lng'))
            self.isAutoGeo = False
        else:
            if self.address is not None:
                self.address = self.address.strip()

        super(Estate, self).save(*args, **kwargs)


@python_2_unicode_compatible
class LandEstate(Estate):
    # -*- характеристики -*-
    appointmentLand = models.ForeignKey(AppointmentLandType, verbose_name="Назначение")
    areaCommon = models.FloatField(_("Общая площадь, сот."))
    isGas = models.BooleanField(_("Доступность газа"), default=False)
    isWater = models.BooleanField(_("Доступность воды"), default=False)
    isLight = models.BooleanField(_("Доступность света"), default=False)

    class Meta:
        db_table = 'land'
        default_related_name = 'lands'
        verbose_name = _("Земельный участок")
        verbose_name_plural = _("Земельные участки")

    def save(self, *args, **kwargs):
        if not self.article.endswith('l'):
            self.article += 'l'

        super(Estate, self).save(*args, **kwargs)
