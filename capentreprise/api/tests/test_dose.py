import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'capentreprise.settings')

# Chargez la configuration de Django
django.setup()
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from django.urls import reverse
from api.views import DWH_api
import json
from capentreprise.settings import TOKEN_LEO

headers_token = {'Authorization': f'Token {TOKEN_LEO}'}

factory = APIRequestFactory()

# region setUp

view = DWH_api.as_view()
url = reverse('api')
url_with_params = f"{url}?table=F_Dose"


# test default table (1 test)
request_default = factory.get(url, headers=headers_token)
date_default_response = view(request_default)
date_default_response.render()
json_response = json.loads(date_default_response.content)

# test whole table (1 tests)
request_pk_whole = factory.get(url_with_params, headers=headers_token)
date_test = view(request_pk_whole)
date_test.render()
json_response_whole = json.loads(date_test.content)

# test with Primary Key (2 tests)
request_pk = factory.get(url_with_params, headers=headers_token)
date_pk_test = view(request_pk, code_PK='AstraZeneca01842021-06-13')
date_pk_test.render()
json_response_pk = json.loads(date_pk_test.content)

# endregion

class Test_Vaccine(TestCase):

    def test_get_default_table(self):
        expected_result = 'F_Dose'
        self.assertEqual(json_response['table_name'], expected_result)
        print(json_response['table_name'])

    def test_get_table_name(self):
        expected_result = 'F_Dose'
        self.assertEqual(json_response_pk['table_name'], expected_result)
        print(json_response_pk['table_name'])

    def test_get_count_dose(self):
        expected_count = 32952
        self.assertEqual(json_response_whole['Nombre de ligne'], expected_count)
        print(json_response_whole['Nombre de ligne'])

    def test_get_data_dose(self):
        expected_result = [{'code_PK': 'AstraZeneca01842021-06-13',
                            'vaccine_type_FK': 'AstraZeneca',
                            'geo_FK': '0184',
                            'count_dose': 3780.0,
                            'date_FK': '2021-06-13',
                            'count_ucd': 378.0
                            }]

        self.assertEqual(json_response_pk['data'], expected_result)
        print(json_response_pk['data'], expected_result)


    def test_get_data_dose_value(self):
        expected_result = 3780.0
        self.assertEqual(json_response_pk['data'][0]['count_dose'], expected_result)
        print(json_response_pk['data'][0]['count_dose'])

