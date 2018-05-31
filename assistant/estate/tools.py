# -*- coding: utf-8 -*-
import random
import sys

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404

from assistant.configuration.model import Configuration
from assistant.estate.model import ApartmentEstate, ResidenceEstate, CommerceEstate, LandEstate
from assistant.estatesettings.model import ConstructionResidenceType, AppointmentType, AppointmentLandType
from assistant.marketing.model import PartnerProgram, Partner
from assistant.settings import MEDIA_URL

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


def get_apartment_estate_list():
    apartment_estates = ApartmentEstate.objects.all()
    if apartment_estates.__len__() > 4:
        apartment_estate_list = random.sample(list(apartment_estates), 4)
    else:
        apartment_estate_list = apartment_estates

    return apartment_estate_list


def get_residence_estate_list():
    residence_estates = ResidenceEstate.objects.all()
    if residence_estates.__len__() > 4:
        residence_estate_list = random.sample(list(residence_estates), 4)
    else:
        residence_estate_list = residence_estates

    return residence_estate_list


def get_commerce_estate_list():
    commerce_estates = CommerceEstate.objects.all()
    if commerce_estates.__len__() > 4:
        commerce_estate_list = random.sample(list(commerce_estates), 4)
    else:
        commerce_estate_list = commerce_estates

    return commerce_estate_list


def get_land_estate_list():
    land_estates = LandEstate.objects.all()
    if land_estates.__len__() > 4:
        land_estate_list = random.sample(list(land_estates), 4)
    else:
        land_estate_list = land_estates

    return land_estate_list


def get_all_estate_context():
    constructions = ConstructionResidenceType.objects.all()
    appointments = AppointmentType.objects.all()
    land_appointments = AppointmentLandType.objects.all()
    apartment_estate_list = get_apartment_estate_list()
    residence_estate_list = get_residence_estate_list()
    land_estate_list = get_land_estate_list()
    commerce_estates_list = get_commerce_estate_list()

    context = {
        'constructions': constructions,
        'appointments': appointments,
        'land_appointments': land_appointments,
        'apartment_estate_list': apartment_estate_list,
        'residence_estate_list': residence_estate_list,
        'commerce_estates_list': commerce_estates_list,
        'land_estate_list': land_estate_list
    }

    context.update(get_partner_horizontal_banner_list())

    return context


def get_estate_context(estate_slug):
    try:
        estate = ApartmentEstate.objects.get(slug=estate_slug)
        caption = estate.caption
        estate_type = 'apartments'
    except ApartmentEstate.DoesNotExist:
        try:
            estate = ResidenceEstate.objects.get(slug=estate_slug)
            caption = estate.construction
            estate_type = 'residences'
        except ResidenceEstate.DoesNotExist:
            try:
                estate = CommerceEstate.objects.get(slug=estate_slug)
                caption = estate.appointment
                estate_type = 'commerces'
            except CommerceEstate.DoesNotExist:
                estate = get_object_or_404(LandEstate, slug=estate_slug)
                caption = estate.appointmentLand
                estate_type = 'lands'

    if Configuration.objects.last() is not None:
        default_phone = Configuration.objects.last().phone
    else:
        default_phone = '-'

    partner_program_list = PartnerProgram.objects.all()

    return {
        'estate': estate,
        'partner_program_list': partner_program_list,
        'caption': caption,
        'default_phone': default_phone,
        'estate_type': estate_type
    }


def get_estate_by_article_context(article):
    try:
        estate = ApartmentEstate.objects.get(article=article)
        caption = estate.caption
        estate_type = 'apartments'
    except ApartmentEstate.DoesNotExist:
        try:
            estate = ResidenceEstate.objects.get(article=article)
            caption = estate.construction
            estate_type = 'residences'
        except ResidenceEstate.DoesNotExist:
            try:
                estate = CommerceEstate.objects.get(article=article)
                caption = estate.appointment
                estate_type = 'commerces'
            except CommerceEstate.DoesNotExist:
                estate = get_object_or_404(LandEstate, article=article)
                caption = estate.appointmentLand
                estate_type = 'lands'

    if Configuration.objects.last() is not None:
        default_phone = Configuration.objects.last().phone
    else:
        default_phone = '-'

    partner_program_list = PartnerProgram.objects.all()

    return {
        'estate': estate,
        'partner_program_list': partner_program_list,
        'caption': caption,
        'default_phone': default_phone,
        'estate_type': estate_type
    }


def get_partner_horizontal_banner_list():
    partner_list = Partner.objects.filter(advertBannerHorizontal__isnull=False, isShowBannerHorizontal=True)
    if partner_list.__len__() > 2:
        partners = random.sample(list(partner_list), 2)
    else:
        partners = partner_list

    if partners.__len__() > 0:
        partner_1 = random.choice(partners)
        partner_2 = random.choice(partners)
        if partners.__len__() == 2:
            while partner_2 == partner_1:
                partner_2 = random.choice(partners)
    else:
        partner_1 = None
        partner_2 = None

    return {
        'partner_1': partner_1,
        'partner_2': partner_2,
        'media_url': MEDIA_URL
    }


def get_catalog_estate_context():
    constructions = ConstructionResidenceType.objects.all()
    appointments = AppointmentType.objects.all()
    land_appointments = AppointmentLandType.objects.all()

    return {
        'constructions': constructions,
        'appointments': appointments,
        'land_appointments': land_appointments
    }


def get_apartments_context(request):
    params = request.GET
    page_num = params.get('page')
    apartment_list = get_apartment_list_by_params(params)
    estates = get_pagination_estate(apartment_list, page_num)

    context = {
        "estate_type": 'apartments',
        'estates': estates,
    }

    context.update(get_additional_context(params.get('colRowView'), page_num))

    return context


def get_apartment_list_by_params(params):
    order_field = params.get('orderField', '0')
    where = 'apartment.region_id=1'
    param_list = []

    where = update_condition_by_param(where, param_list, params.get('isRoom'), ' and apartment.isRoom=1', True)
    where = update_condition_by_param(where,
                                      param_list,
                                      params.get('countRoom'), ' and apartment.room=%s and apartment.isRoom=0', False)
    where = update_condition_by_param(where, param_list, params.get('isFiveRoom'), ' and apartment.isRoom>=5', True)
    where = update_condition_by_param(where, param_list, params.get('city'), ' and apartment.city_id=%s', False)
    where = update_condition_by_param(where, param_list, params.get('district'), ' and apartment.district_id=%s', False)
    where = update_condition_by_param(where, param_list, params.get('street'), ' and apartment.street_id=%s', False)
    where = update_condition_by_param(where, param_list, params.get('costMin'), ' and apartment.cost>=%s', False)
    where = update_condition_by_param(where, param_list, params.get('costMax'), ' and apartment.cost<=%s', False)
    where = update_condition_by_param(where, param_list, params.get('areaMin'), ' and apartment.areaCommon>=%s', False)
    where = update_condition_by_param(where, param_list, params.get('areaMax'), ' and apartment.areaCommon<=%s', False)
    where = update_condition_by_list_param(where,
                                           param_list,
                                           params.get('construction'), ' and apartment.construction_id in (')

    apartment_list = ApartmentEstate.objects.extra(where=[where], params=tuple(param_list))

    if order_field == '0':
        return apartment_list.order_by('pk')
    elif order_field == '1':
        return apartment_list.order_by('city__name', 'street__name', 'number')
    else:
        return apartment_list.order_by('cost')


def get_residence_context(request):
    params = request.GET
    page_num = params.get('page')
    residence_list = get_residence_list_by_params(params)
    estates = get_pagination_estate(residence_list, page_num)

    context = {
        "estate_type": 'residences',
        'estates': estates,
    }

    context.update(get_additional_context(params.get('colRowView'), page_num))

    return context


def get_residence_list_by_params(params):
    order_field = params.get('orderField', '0')
    where = 'residence.region_id=1'
    param_list = []

    where = update_condition_by_param(where, param_list, params.get('city'), ' and residence.city_id=%s', False)
    where = update_condition_by_param(where, param_list, params.get('district'), ' and residence.district_id=%s', False)
    where = update_condition_by_param(where, param_list, params.get('street'), ' and residence.street_id=%s', False)
    where = update_condition_by_param(where, param_list, params.get('costMin'), ' and residence.cost>=%s', False)
    where = update_condition_by_param(where, param_list, params.get('costMax'), ' and residence.cost<=%s', False)
    where = update_condition_by_param(where, param_list, params.get('areaMin'), ' and residence.areaCommon>=%s', False)
    where = update_condition_by_param(where, param_list, params.get('areaMax'), ' and residence.areaCommon<=%s', False)
    where = update_condition_by_list_param(where,
                                           param_list, params.get('construction'), ' and residence.construction_id in (')

    commerce_list = ResidenceEstate.objects.extra(where=[where], params=tuple(param_list))

    if order_field == '0':
        return commerce_list.order_by('pk')
    elif order_field == '1':
        return commerce_list.order_by('city__name', 'street__name', 'number')
    else:
        return commerce_list.order_by('cost')


def get_commerce_context(request):
    params = request.GET
    page_num = params.get('page')
    commerce_list = get_commerce_list_by_params(params)
    estates = get_pagination_estate(commerce_list, page_num)

    context = {
        "estate_type": 'commerces',
        'estates': estates,
    }

    context.update(get_additional_context(params.get('colRowView'), page_num))

    return context


def get_commerce_list_by_params(params):
    order_field = params.get('orderField', '0')
    where = 'commerce.region_id=1'
    param_list = []

    where = update_condition_by_param(where, param_list, params.get('city'), ' and commerce.city_id=%s', False)
    where = update_condition_by_param(where, param_list, params.get('district'), ' and commerce.district_id=%s', False)
    where = update_condition_by_param(where, param_list, params.get('street'), ' and commerce.street_id=%s', False)
    where = update_condition_by_param(where, param_list, params.get('costMin'), ' and commerce.cost>=%s', False)
    where = update_condition_by_param(where, param_list, params.get('costMax'), ' and commerce.cost<=%s', False)
    where = update_condition_by_param(where, param_list, params.get('areaMin'), ' and commerce.areaCommon>=%s', False)
    where = update_condition_by_param(where, param_list, params.get('areaMax'), ' and commerce.areaCommon<=%s', False)
    where = update_condition_by_list_param(where,
                                           param_list, params.get('appointment'), ' and commerce.appointment_id in (')
    where = update_condition_by_list_param(where,
                                           param_list,
                                           params.get('construction'),
                                           ' and commerce.constructionCommerce_id in (')

    commerce_list = CommerceEstate.objects.extra(where=[where], params=tuple(param_list))

    if order_field == '0':
        return commerce_list.order_by('pk')
    elif order_field == '1':
        return commerce_list.order_by('city__name', 'street__name', 'number')
    else:
        return commerce_list.order_by('cost')


def get_lands_context(request):
    params = request.GET
    page_num = params.get('page')
    land_list = get_land_list_by_params(params)
    estates = get_pagination_estate(land_list, page_num)

    context = {
        "estate_type": 'lands',
        'estates': estates,
    }

    context.update(get_additional_context(params.get('colRowView'), page_num))

    return context


def get_land_list_by_params(params):
    order_field = params.get('orderLandField', '0')
    where = 'land.region_id=1'
    param_list = []

    where = update_condition_by_param(where, param_list, params.get('city'), ' and land.city_id=%s', False)
    where = update_condition_by_param(where, param_list, params.get('costMin'), ' and land.cost>=%s', False)
    where = update_condition_by_param(where, param_list, params.get('costMax'), ' and land.cost<=%s', False)
    where = update_condition_by_param(where, param_list, params.get('areaMin'), ' and land.areaCommon>=%s', False)
    where = update_condition_by_param(where, param_list, params.get('areaMax'), ' and land.areaCommon<=%s', False)
    where = update_condition_by_list_param(where,
                                           param_list,
                                           params.get('appointmentLand'), ' and land.appointmentLand_id in (')

    land_list = LandEstate.objects.extra(where=[where], params=tuple(param_list))

    if order_field == '0':
        return land_list.order_by('pk')
    elif order_field == '1':
        return land_list.order_by('city__name')
    else:
        return land_list.order_by('cost')


def update_condition_by_param(where, param_list, param, statement, is_boolean):
    if param is not None and param != "":
        where += statement
        if not is_boolean:
            param_list.append(param)

    return where


def update_condition_by_list_param(where, param_list, param, statement):
    if param is not None and param != "":
        split_list = str(param).split(',')
        for idx, item in enumerate(split_list):
            statement += '%s'
            if idx != len(split_list) - 1:
                statement += ','
            param_list.append(item)
        statement += ')'
        where += statement

    return where


def get_pagination_estate(estate_list, page_num):
    paginator = Paginator(estate_list, 12)

    try:
        estates = paginator.page(page_num)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        estates = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        estates = paginator.page(paginator.num_pages)

    return estates


def get_additional_context(col_row_view_type, page_num):
    if col_row_view_type is not None:
        col_row_view = col_row_view_type
    else:
        col_row_view = "0"

    if is_integer(page_num):
        page_back_limit = int(page_num) - 6
        page_forward_limit = int(page_num) + 6
    else:
        page_back_limit = 1
        page_forward_limit = 6

    return {
        "page_back_limit": page_back_limit,
        "page_forward_limit": page_forward_limit,
        "col_row_view": col_row_view,
    }


def is_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def get_json_apartment_geo():
    result = []
    apartments = ApartmentEstate.objects.all()
    for apartment in apartments:
        if apartment.literal is None:
            literal = ''
        else:
            literal = ' ' + apartment.literal

        geo = str(apartment.geolocation)
        index = get_index_by_geo(result, geo, apartment.address)

        if index is None:
            result.append({
                'count': 1,
                'address': apartment.address,
                'geo': geo,
                'address_show': apartment.street.__str__() + ', ' + str(apartment.number) + literal,
                'objects': [{
                    'caption': apartment.caption,
                    'slug': apartment.slug
                }],
            })
        else:
            result[index]['count'] += 1
            result[index]['objects'].append({
                'caption': apartment.caption,
                'slug': apartment.slug
            })

    return {'result': result}


def get_json_residence_geo():
    result = []
    residences = ResidenceEstate.objects.all()
    for residence in residences:
        if residence.literal is None:
            literal = ''
        else:
            literal = ' ' + residence.literal

        geo = str(residence.geolocation)
        index = get_index_by_geo(result, geo, residence.address)

        if index is None:
            result.append({
                'count': 1,
                'address': residence.address,
                'geo': geo,
                'address_show': residence.street.__str__() + ', ' + str(residence.number) + literal,
                'objects': [{
                    'caption': residence.construction.__str__(),
                    'slug': residence.slug
                }],
            })
        else:
            result[index]['count'] += 1
            result[index]['objects'].append({
                'caption': residence.construction.__str__(),
                'slug': residence.slug
            })

    return {'result': result}


def get_json_commerce_geo():
    result = []
    commerces = CommerceEstate.objects.all()
    for commerce in commerces:
        if commerce.literal is None:
            literal = ''
        else:
            literal = ' ' + commerce.literal

        geo = str(commerce.geolocation)
        index = get_index_by_geo(result, geo, commerce.address)

        if index is None:
            result.append({
                'count': 1,
                'address': commerce.address,
                'geo': geo,
                'address_show': commerce.street.__str__() + ', ' + str(commerce.number) + literal,
                'objects': [{
                    'caption': commerce.appointment.__str__(),
                    'slug': commerce.slug
                }],
            })
        else:
            result[index]['count'] += 1
            result[index]['objects'].append({
                'caption': commerce.appointment.__str__(),
                'slug': commerce.slug
            })

    return {'result': result}


def get_json_land_geo():
    result = []
    lands = LandEstate.objects.all()
    for land in lands:
        geo = str(land.geolocation)
        index = get_index_by_geo(result, geo, None)

        if index is None:
            result.append({
                'count': 1,
                'geo': geo,
                'objects': [{
                    'caption': land.appointmentLand.__str__(),
                    'slug': land.slug
                }],
            })
        else:
            result[index]['count'] += 1
            result[index]['objects'].append({
                'caption': land.appointmentLand.__str__(),
                'slug': land.slug
            })

    return {'result': result}


def get_index_by_geo(array, geo, address):
    for index, item in enumerate(array):
        if item.get('geo') == geo or item.get('address') == address:
            return index
    else:
        return None
