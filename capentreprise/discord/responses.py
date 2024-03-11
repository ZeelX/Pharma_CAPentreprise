from datetime import datetime, timedelta
from random import choice, randint

from django.db.models import Q

from data_parser.models import F_Dose

total = 0
date_now = datetime.now()
date_3_year = date_now - timedelta(days=365.25 * 3)

day_3_year = date_3_year.weekday()
if day_3_year == 6:
    sunday_3_year = date_3_year
else:
    diff = 6 - day_3_year
    sunday_3_year = date_3_year + timedelta(days=diff)
    # les dates ont 1 semaine de décalage par rapporta  2021
    sunday_3_year = sunday_3_year + timedelta(days=7)
sunday_3_year = sunday_3_year.strftime('%Y-%m-%d')
dose_week = F_Dose.objects.filter(Q(date_FK_id=sunday_3_year), Q(geo_FK_id=6384))

for dose in dose_week:
    total = total + dose.count_dose


def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == '':
        return "Why so silent ..?"

    elif 'doses' in lowered:
        return (f'Le nombre de doses total demandé est de {int(total)} pour le puy de dôme! Checks le code sur https://github.com/ZeelX/Pharma_CAPentreprise/tree/dev')

    elif 'hello' in lowered:
        return "Hello Boi !"
    else:
        return choice(['I do not understand...', 'What are you talking about ?', 'Do you mind rephrasing that ?'])



