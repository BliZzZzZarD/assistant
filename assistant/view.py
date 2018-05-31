# -*- coding: utf-8 -*-
import sys

from django.core.mail import BadHeaderError, send_mail
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from assistant import settings
from assistant.address.tools import get_streets_context, get_cities_context, get_districts_context
from assistant.estate.tools import get_json_apartment_geo, get_apartments_context, get_json_land_geo, get_lands_context, \
    get_commerce_context, get_json_commerce_geo, get_json_residence_geo, get_residence_context
from assistant.estatesettings.tools import get_constructions_context, get_land_appointment_context, \
    get_appointments_context, get_commerce_constructions_context, get_residence_constructions_context
from assistant.tools import get_main_context, get_configuration, get_contact_context, get_calculator_context

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


def index(request):
    context = get_main_context()
    return render(request, 'main.html', context)


def contact(request):
    return render(request, 'contact.html', get_contact_context())


def calculator(request, cost=None):
    return render(request, 'calculator.html', get_calculator_context(cost))


def configuration(request):
    return JsonResponse({'data': get_configuration()})


def get_apartment_geo(request):
    return JsonResponse({'data': get_json_apartment_geo()})


def get_apartments(request):
    context = get_apartments_context(request)
    return render(request, 'estate/estates_catalog.html', context)


def get_cities(request):
    context = get_cities_context()
    return render(request, 'utils/options.html', context)


def get_districts(request):
    context = get_districts_context(request)
    return render(request, 'utils/options.html', context)


def get_streets(request):
    context = get_streets_context(request)
    return render(request, 'utils/options.html', context)


def get_constructions(request):
    context = get_constructions_context()
    return render(request, 'utils/options.html', context)


def get_residences(request):
    context = get_residence_context(request)
    return render(request, 'estate/estates_catalog.html', context)


def get_residence_geo(request):
    return JsonResponse({'data': get_json_residence_geo()})


def get_residence_constructions(request):
    context = get_residence_constructions_context()
    return render(request, 'utils/options.html', context)


def get_commerces(request):
    context = get_commerce_context(request)
    return render(request, 'estate/estates_catalog.html', context)


def get_commerce_geo(request):
    return JsonResponse({'data': get_json_commerce_geo()})


def get_commerce_constructions(request):
    context = get_commerce_constructions_context()
    return render(request, 'utils/options.html', context)


def get_appointments(request):
    context = get_appointments_context()
    return render(request, 'utils/options.html', context)


def get_land_geo(request):
    return JsonResponse({'data': get_json_land_geo()})


def get_lands(request):
    context = get_lands_context(request)
    return render(request, 'estate/estates_catalog.html', context)


def get_land_appointment(request):
    context = get_land_appointment_context()
    return render(request, 'utils/options.html', context)


@csrf_protect
def send_email(request):
    person = request.POST.get('person', '')
    email = request.POST.get('email', '')
    phone = request.POST.get('phone', '')
    text = request.POST.get('text', '')

    subject = "Отправка с формы обратной связи"
    message = "Имя: " + person + "\n" + "Телефон: " + phone + "\n" + "Email: " + email + "\n" + "Сообщение: " + text

    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
    except BadHeaderError:
        return HttpResponse("При отправки письма произошла ошибка")

    return HttpResponse("OK")


@csrf_protect
def send_wait_call(request):
    text = request.POST.get('text', '')

    subject = "ЖДУ ЗВОНКА!!!"

    try:
        send_mail(subject, text, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
    except BadHeaderError:
        return HttpResponse("При отправке формы произошла ошибка")

    return HttpResponse("OK")
