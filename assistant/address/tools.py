# -*- coding: utf-8 -*-
import sys

from assistant.address.model import City, Street, District

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


def get_cities_context():
    options = []
    city_set = City.objects.filter(region__id=1)
    for city in city_set:
        options.append({'value': city.id, 'label': city.name})

    return {'options': options}


def get_districts_context(request):
    options = []
    params = request.GET

    district_set = District.objects.filter(region__id=params.get('cityValue'))

    for district in district_set:
        options.append({'value': district.id, 'label': district.name})

    return {'options': options}


def get_streets_context(request):
    options = []
    params = request.GET

    if params.get('districtValue') == '':
        street_set = Street.objects.filter(city__id=params.get('cityValue'))
    else:
        street_set = Street.objects.filter(city__id=params.get('cityValue'), district__id=params.get('districtValue'))

    for street in street_set:
        options.append({'value': street.id, 'label': street.name})

    return {'options': options}
