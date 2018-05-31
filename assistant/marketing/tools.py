# -*- coding: utf-8 -*-
import random
import sys

from django.db.models import Q
from django.shortcuts import get_object_or_404

from assistant.marketing.model import BannerHorizontal, BannerVertical, Partner, PartnerProgram

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


def get_horizontal_banner_url():
    banners = BannerHorizontal.objects.filter(isShow=True)
    if banners.__len__() > 1:
        banner_url = random.choice(list(banners)).picture.url
    elif banners.__len__() == 1:
        banner_url = list(banners)[0].picture.url
    else:
        banner_url = None

    return banner_url


def get_vertical_banner_url():
    banners = BannerVertical.objects.filter(isShow=True)
    if banners.__len__() > 1:
        banner_url = random.choice(list(banners)).picture.url
    elif banners.__len__() == 1:
        banner_url = list(banners)[0].picture.url
    else:
        banner_url = None

    return banner_url


def get_all_partner_context():
    return {
        'bank_partner_list': Partner.objects.filter(type__name='Банк'),
        'building_partner_list': Partner.objects.filter(type__name='Строительная организация'),
        'other_partner_list': Partner.objects.exclude(Q(type__name='Банк') | Q(type__name='Строительная организация'))
    }


def get_partner_context(partner_slug):
    try:
        partner = Partner.objects.get(slug=partner_slug)
    except Partner.DoesNotExist:
        partner = get_object_or_404(Partner, slug=partner_slug)

    partner_program_list = PartnerProgram.objects.filter(partner=partner)

    return {
        'partner': partner,
        'partner_program_list': partner_program_list,
    }


def get_program_context(partner_slug):
    try:
        program = PartnerProgram.objects.get(slug=partner_slug)
    except PartnerProgram.DoesNotExist:
        program = get_object_or_404(PartnerProgram, slug=partner_slug)

    return {
        'program': program
    }


def get_partner_program_context(partner=None):
    if partner is not None:
        partner_program_list = PartnerProgram.objects.filter(partner=partner)
    else:
        partner_program_list = PartnerProgram.objects.all()

    return {
        'partner_program_list': partner_program_list
    }


def get_mortgage_price_context_by_partner_list(cost):
    partner_program_list = PartnerProgram.objects.all()

    for program in partner_program_list:
        program.price = get_mortgage_price_context(cost, program.rate, program.term)

    return {'partner_program_list': partner_program_list}


def get_mortgage_price_context(cost, rate=None, term=None):
    if rate is None:
        rate = get_best_rate()

    if rate is not None:
        if term is not None:
            mp_cnt = term * 12
        else:
            mp_cnt = 30 * 12
        rate = rate / 1200.0
        ak = (rate * (1 + rate) ** mp_cnt) / (((1 + rate) ** mp_cnt) - 1)
        mp = cost * ak
        mortgage_price = round(mp, 2)
    else:
        mortgage_price = '-'

    return mortgage_price


def get_best_rate():
    programs = PartnerProgram.objects.all()
    if len(programs) > 0:
        rate = programs[0].rate
        for program in programs:
            if rate > program.rate:
                rate = program.rate
    else:
        rate = None

    return rate
