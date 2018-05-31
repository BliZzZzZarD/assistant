# -*- coding: utf-8 -*-
import sys

from django.shortcuts import render

from assistant.marketing.tools import get_all_partner_context, get_partner_context, get_program_context

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


def show_all_partner(request):
    context = get_all_partner_context()
    return render(request, 'partner/allPartner.html', context)


def show_partner(request, partner_slug):
    context = get_partner_context(partner_slug)
    return render(request, 'partner/partner.html', context)


def show_program(request, program_slug):
    context = get_program_context(program_slug)
    return render(request, 'partner_program/partner_program.html', context)


