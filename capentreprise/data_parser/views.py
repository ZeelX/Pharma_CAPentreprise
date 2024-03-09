from django.shortcuts import render
from data_parser.models import ODS, F_Dose
from django.db.models import Q
from datetime import datetime, timedelta

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

# Create your views here.
def index(request):
    total = 0
    date_now = datetime.now()
    date_3_year = date_now - timedelta(days=365.25 * 3)

    day_3_year = date_3_year.weekday()
    print(day_3_year)
    if day_3_year == 6:
        sunday_3_year = date_3_year
    else:
        diff = 6 - day_3_year
        sunday_3_year = date_3_year + timedelta(days=diff)
        # les dates ont 1 semaine de décalage par rapporta  2021
        sunday_3_year = sunday_3_year + timedelta(days=7)
    print(sunday_3_year)
    sunday_3_year = sunday_3_year.strftime('%Y-%m-%d')
    dose_week = F_Dose.objects.filter(Q(date_FK_id=sunday_3_year), Q(geo_FK_id=6384))

    for dose in dose_week:
        total = total + dose.count_dose

    context = {'dose': total, 'request': request}
    return render(request, 'index.html', context=context)
#
# def result(request, code_get):
#     total = 0
#     date_now = datetime.now()
#     date_3_year = date_now - timedelta(days=365.25 * 3)
#     day_3_year = date_3_year.weekday()
#     print(day_3_year)
#     if day_3_year == 6:
#         sunday_3_year = date_3_year
#     else:
#         diff = 6 - day_3_year
#         sunday_3_year = date_3_year + timedelta(days=diff)
#     print(sunday_3_year)
#     sunday_3_year = sunday_3_year.strftime('%Y-%m-%d')
#     dose_week = F_Dose.objects.filter(Q(date_FK_id=sunday_3_year), Q(geo_FK_id=6384))
#
#     for dose in dose_week:
#         total = total + dose.count_dose
#
#     context = {'dose': total, 'request': request}
#     return render(request, 'index.html', context=context)
