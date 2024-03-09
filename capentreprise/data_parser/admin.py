from django.contrib import admin
from data_parser.models import D_Geo,D_Date,D_Vaccine_Type,F_Dose

# Register your models here.
admin.site.register(D_Geo),
admin.site.register(D_Date),
admin.site.register(D_Vaccine_Type),
admin.site.register(F_Dose)