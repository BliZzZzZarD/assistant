# -*- coding: utf-8 -*-
import sys
from django import template

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")

register = template.Library()


@register.inclusion_tag("tags/wait_call.html")
def wait_call():
    text_message = "Устали искать? Оставьте телефон, и мы сами вам позвоним:"
    return {"text_message": text_message}


@register.inclusion_tag("tags/article_search.html")
def article_search():
    text_message = "Знаете код объекта? Быстрый переход на страницу:"
    return {"text_message": text_message}


@register.inclusion_tag("tags/header_page.html")
def header_page(caption):
    return {"caption": caption}


@register.inclusion_tag("tags/calculator.html")
def calculator():
    return {}
