# -*- coding: UTF-8 -*-
import sys
from django import template

from assistant.additionalpage.tools import get_pages_navigation_context
from assistant.estate.tools import get_catalog_estate_context

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


register = template.Library()


@register.inclusion_tag("tags/navigation.html")
def navigation():
    return get_pages_navigation_context()


@register.inclusion_tag("tags/estate_catalog_navigation.html")
def estate_catalog_navigation():
    return get_catalog_estate_context()
