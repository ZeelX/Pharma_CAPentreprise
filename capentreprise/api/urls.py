from django.urls import path
from api.views import DWH_api

urlpatterns = [
    path('dwh/', DWH_api.as_view()),

]

