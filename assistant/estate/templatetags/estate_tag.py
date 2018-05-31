# -*- coding: UTF-8 -*-
import sys
from django import template

from assistant.marketing.tools import get_mortgage_price_context

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")

register = template.Library()


@register.inclusion_tag("tags/price.html")
def price(cost, area):
    return {'price': round(cost/area, 2)}


@register.inclusion_tag("tags/mortgage_price.html")
def mortgage_price(cost):
    return {'mortgage_price': get_mortgage_price_context(cost)}


@register.inclusion_tag("tags/price_row.html")
def price_row(cost, area):
    return {'price': round(cost/area, 2)}


@register.inclusion_tag("tags/mortgage_price_row.html")
def mortgage_price_row(cost):
    return {'mortgage_price': get_mortgage_price_context(cost)}


@register.inclusion_tag("tags/cost_service.html")
def cost_service(cost):
    return {'cost': cost}


@register.inclusion_tag("estate/apartments/apartment_info_block.html")
def apartment_info_block(estate):
    return {'estate': estate}


@register.inclusion_tag("estate/residences/residence_info_block.html")
def residence_info_block(estate):
    return {'estate': estate}


@register.inclusion_tag("estate/commerces/commerce_info_block.html")
def commerce_info_block(estate):
    return {'estate': estate}


@register.inclusion_tag("estate/lands/land_info_block.html")
def land_info_block(estate):
    return {'estate': estate}


@register.inclusion_tag("estate/estate_col.html")
def estate_col(estate, caption):
    return {
        'estate': estate,
        'caption': caption
    }


@register.inclusion_tag("estate/apartments/apartment_col.html")
def apartment_col(apartment):
    return {'apartment': apartment}


@register.inclusion_tag("estate/residences/residence_col.html")
def residence_col(residence):
    return {'residence': residence}


@register.inclusion_tag("estate/commerces/commerce_col.html")
def commerce_col(commerce):
    return {'commerce': commerce}


@register.inclusion_tag("estate/lands/land_col.html")
def land_col(land):
    return {'land': land}


@register.inclusion_tag("estate/estate_row.html")
def estate_row(estate, caption):
    return {
        'estate': estate,
        'caption': caption
    }


@register.inclusion_tag("estate/estate_view_sort_tag.html")
def estate_view_sort_tag():
    return {}


@register.inclusion_tag("estate/apartments/apartment_row.html")
def apartment_row(estate):
    return {'apartment': estate}


@register.inclusion_tag("estate/residences/residence_row.html")
def residence_row(estate):
    return {'residence': estate}


@register.inclusion_tag("estate/commerces/commerce_row.html")
def commerce_row(estate):
    return {'commerce': estate}


@register.inclusion_tag("estate/lands/land_row.html")
def land_row(estate):
    return {'land': estate}


@register.inclusion_tag("tags/pagination.html")
def pagination(estates, page_back_limit, page_forward_limit, estate_type):
    return {
        'estates': estates,
        "page_back_limit": page_back_limit,
        "page_forward_limit": page_forward_limit,
        'estate_type': estate_type
    }
