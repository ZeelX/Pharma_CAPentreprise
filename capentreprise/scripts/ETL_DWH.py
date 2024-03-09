import os
import django
import sqlite3
import pandas as pd
import time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'capentreprise.settings')

django.setup()

from data_parser.models import ODS, D_Vaccine_Type, D_Geo, D_Date, F_Dose
from django.db.models import Q
from datetime import datetime


def extract_data_ods():
     return ODS.objects.filter(~Q(nb_ucd='nan'),~Q(nb_ucd='NA'))

start_time = time.time()
existing_keys = set()

# Table de Dimension =>
# Table D_Vaccine_Type
print("Vaccine Type Extraction")
D_Vaccine_Type.objects.all().delete()
vaccine_type_list = []

for data_vaccin in extract_data_ods():
    pk_check_vaccin = data_vaccin.type_de_vaccin
    if pk_check_vaccin not in existing_keys:
        vaccine_instance = D_Vaccine_Type(
            code_PK=data_vaccin.type_de_vaccin
        )
        vaccine_type_list.append(vaccine_instance)
        existing_keys.add(pk_check_vaccin)

print("Vaccine Type bulk")

D_Vaccine_Type.objects.bulk_create(vaccine_type_list)

# Table D_Date
print("Date Extraction")

D_Date.objects.all().delete()
date_list = []
existing_keys.clear()

for data_date in extract_data_ods():
    pk_check_date = data_date.date_fin_semaine
    if pk_check_date not in existing_keys:
        date_instance = D_Date(
            code_PK=data_date.date_fin_semaine
        )
        date_list.append(date_instance)
        existing_keys.add(pk_check_date)
print("Date bulk")

D_Date.objects.bulk_create(date_list)

# Table D_Geo
print("Geo Extraction")

D_Geo.objects.all().delete()
geo_list = []
existing_keys.clear()


for data_geo in extract_data_ods():
    pk_check_geo = data_geo.code_departement.zfill(2) + data_geo.code_region
    if pk_check_geo not in existing_keys:
        date_instance = D_Geo(
            code_PK=pk_check_geo,
            code_departement=data_geo.code_departement,
            code_region=data_geo.code_region,
            libelle_departement=data_geo.libelle_departement,
            libelle_region=data_geo.libelle_region,
        )
        geo_list.append(date_instance)
        existing_keys.add(pk_check_geo)

print("Geo bulk")
D_Geo.objects.bulk_create(geo_list)

# Table de Fait
# Table F_Dose
print("Dose Extraction")

F_Dose.objects.all().delete()
dose_list = []
existing_keys.clear()

for data_dose in extract_data_ods():

    pk_check_dose = data_dose.type_de_vaccin + data_dose.code_departement.zfill(2) + data_dose.code_region + str(data_dose.date_fin_semaine)
    if pk_check_dose not in existing_keys:
        vaccine_obj_instance, created = D_Vaccine_Type.objects.get_or_create(code_PK=data_dose.type_de_vaccin)
        geo_obj_instance, created = D_Geo.objects.get_or_create(code_PK=data_dose.code_departement.zfill(2) + data_dose.code_region)
        date_obj_instance, created = D_Date.objects.get_or_create(code_PK=data_dose.date_fin_semaine)

        dose_instance = F_Dose(
            code_PK=pk_check_dose,
            vaccine_type_FK=vaccine_obj_instance,
            geo_FK=geo_obj_instance,
            date_FK=date_obj_instance,
            count_dose=data_dose.nb_doses,
            count_ucd=data_dose.nb_ucd,
        )
        dose_list.append(dose_instance)
        existing_keys.add(pk_check_dose)

print("Dose bulk")

F_Dose.objects.bulk_create(dose_list)


end_time = time.time()
execution_time = end_time - start_time
print(f" {execution_time} seconds to finish")
