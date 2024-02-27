import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'capentreprise.settings')
django.setup()

from data_parser.models import ODS
import pandas as pd
from capentreprise.settings import DATA_DIR

csv_file_path = os.path.join(DATA_DIR, 'flux-total-dep.csv')
df = pd.read_csv(csv_file_path, sep=',',encoding='ISO-8859-1')
ODS.objects.all().delete()

ods_objects = []
for index, row in df.iterrows():
    ods = ODS(
        code_region=row['code_region'],
        libelle_region=row['libelle_region'],
        code_departement=row['code_departement'],
        libelle_departement=row['libelle_departement'],
        date_fin_semaine=row['date_fin_semaine'],
        type_de_vaccin=row['type_de_vaccin'],
        nb_ucd=row['nb_ucd'],
        nb_doses=row['nb_doses'],

    )
    ods_objects.append(ods)
ODS.objects.bulk_create(ods_objects)

