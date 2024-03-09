
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'capentreprise.settings')

# Chargez la configuration de Django
django.setup()
from django.shortcuts import render
from data_parser.models import ODS, F_Dose
from django.db.models import Q
from datetime import datetime, timedelta

from django.test import TestCase

total = 0
date_now = datetime.now()
date_3_year = date_now - timedelta(days=365.2425 * 3)
day_3_year = date_3_year.weekday()
print(day_3_year)
if day_3_year == 0:
    sunday_3_year = date_3_year
else:
    diff = 6 - day_3_year
    sunday_3_year = date_3_year + timedelta(days=diff)
print(sunday_3_year)
sunday_3_year = sunday_3_year.strftime('%Y-%m-%d')
dose_week = F_Dose.objects.filter(Q(date_FK_id=sunday_3_year), Q(geo_FK_id= 6384))



