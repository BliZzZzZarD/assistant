# -*- coding: UTF-8 -*-
import sys

from django import template

from assistant.marketing.tools import get_horizontal_banner_url, get_vertical_banner_url, get_partner_program_context, \
    get_mortgage_price_context_by_partner_list

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")

register = template.Library()


@register.inclusion_tag("tags/banner_horizontal.html")
def horizontal_banner():
    return {'banner_url': get_horizontal_banner_url()}


@register.inclusion_tag("tags/banner_vertical.html")
def vertical_banner():
    return {'banner_url': get_vertical_banner_url()}


@register.inclusion_tag("tags/partner_program_estate_page.html")
def partner_program_estate_page(cost):
    return get_mortgage_price_context_by_partner_list(cost)


@register.inclusion_tag("tags/partner_program.html")
def partner_program(partner=None):
    return {'partner': partner}


@register.inclusion_tag("tags/partner_program_table.html")
def partner_program_table(partner=None):
    return get_partner_program_context(partner)


@register.inclusion_tag("tags/partner_horizontal.html")
def partner_horizontal(partner, media_url):
    return {
        'partner': partner,
        'media_url': media_url
    }


@register.inclusion_tag("tags/partner_item.html")
def partner_item(partner):
    return {'partner': partner}



