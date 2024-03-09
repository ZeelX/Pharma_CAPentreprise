from django.shortcuts import render
from data_parser.models import ODS, F_Dose, D_Date, D_Geo
from django.db.models import Q
from datetime import datetime, timedelta

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
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

    context = {'date': sunday_3_year, 'departement': 'Puy de Dôme', 'dose': int(total), 'request': request}
    return render(request, 'index.html', context=context)

def research(request):

    date = D_Date.objects.all()

    date_list = []
    for item in date:
        date_list.append(item.code_PK)

    departement = D_Geo.objects.all()
    departement_list = []
    for item in departement:
        departement_list.append(item.libelle_departement)

    context = {'date': date_list, 'departement': departement_list}
    return render(request, 'form_search.html', context=context)

def result(request):


    if request.method == 'POST':
        total = 0
        date = request.POST.get('date', '')
        departement = request.POST.get('departement', '')
        geo_PK = D_Geo.objects.filter(Q(libelle_departement=departement))

        dose_week = F_Dose.objects.filter(Q(date_FK_id=date), Q(geo_FK_id=geo_PK.first()))
        for dose in dose_week:
            total = total + dose.count_dose

        context = {'date': date, 'departement': departement, 'dose': int(total)}
        return render(request, 'result.html', context=context)
    else:

        return render(request, 'result.html')
