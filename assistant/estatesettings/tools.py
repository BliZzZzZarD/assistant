# -*- coding: utf-8 -*-
import sys

from assistant.estatesettings.model import ConstructionType, AppointmentLandType, AppointmentType, \
    ConstructionCommerceType, ConstructionResidenceType

if sys.version.startswith("2"):
    reload(sys)
    sys.setdefaultencoding("utf-8")


def get_constructions_context():
    options = []
    result_set = ConstructionType.objects.all()
    for result in result_set:
        options.append({'value': result.id, 'label': result.name})

    return {'options': options}


def get_residence_constructions_context():
    options = []
    result_set = ConstructionResidenceType.objects.all()
    for result in result_set:
        options.append({'value': result.id, 'label': result.name})

    return {'options': options}


def get_commerce_constructions_context():
    options = []
    result_set = ConstructionCommerceType.objects.all()
    for result in result_set:
        options.append({'value': result.id, 'label': result.name})

    return {'options': options}


def get_appointments_context():
    options = []
    result_set = AppointmentType.objects.all()
    for result in result_set:
        options.append({'value': result.id, 'label': result.name})

    return {'options': options}


def get_land_appointment_context():
    options = []
    result_set = AppointmentLandType.objects.all()
    for result in result_set:
        options.append({'value': result.id, 'label': result.name})

    return {'options': options}

