# -*- coding: utf-8 -*-
import sys

from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from assistant.estate.model import ApartmentEstate, ResidenceEstate, CommerceEstate, LandEstate
from assistant.service.model import Service

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


class ApartmentSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return ApartmentEstate.objects.all()

    def location(self, obj):
        return obj.slug


class ResidenceSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return ResidenceEstate.objects.all()

    def location(self, obj):
        return obj.slug


class CommerceSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return CommerceEstate.objects.all()

    def location(self, obj):
        return obj.slug


class LandSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return LandEstate.objects.all()

    def location(self, obj):
        return obj.slug


class ServiceSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Service.objects.all()

    def location(self, obj):
        return obj.slug


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['index', 'contact', 'show_all_service', 'show_all_estate', 'show_all_partner']

    def location(self, item):
        return reverse(item)
