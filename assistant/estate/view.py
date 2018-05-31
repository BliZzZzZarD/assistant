# -*- coding: utf-8 -*-
import sys

from django.shortcuts import render

from assistant.estate.tools import get_all_estate_context, get_estate_context, get_estate_by_article_context

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


def show_all_estate(request):
    return render(request, 'estate/allEstate.html', get_all_estate_context())


def show_apartments(request):
    return render(request, 'estate/apartments/apartment_category.html')


def show_residences(request):
    return render(request, 'estate/residences/residence_category.html')


def show_commerces(request):
    return render(request, 'estate/commerces/commerce_category.html')


def show_lands(request):
    return render(request, 'estate/lands/land_category.html')


def show_estate(request, estate_slug):
    return render(request, 'estate/estate.html', get_estate_context(estate_slug))


def show_estate_by_article(request, article):
    return render(request, 'estate/estate.html', get_estate_by_article_context(article))


