from django.db import models


# Create your models here.
class ODS(models.Model):
    code_region = models.CharField(max_length=255, default=None)
    libelle_region = models.CharField(max_length=255, default=None)
    code_departement = models.CharField(max_length=255, default=None)
    libelle_departement = models.CharField(max_length=255, default=None)
    date_fin_semaine = models.DateField(default='1900-01-01', null=True)
    type_de_vaccin = models.CharField(max_length=255, default=None)
    nb_ucd = models.CharField(max_length=255, default=None)
    nb_doses = models.CharField(max_length=255, default=None)

class D_Vaccine_Type(models.Model):
    code_PK = models.CharField(max_length=255, default=None, primary_key=True, unique=True)

class D_Geo(models.Model):
    # PK = code_departement + code_region
    code_PK = models.CharField(max_length=255, default=None, primary_key=True, unique=True)
    code_departement = models.CharField(max_length=255, default=None)
    code_region = models.CharField(max_length=255, default=None)
    libelle_departement = models.CharField(max_length=255, default=None)
    libelle_region = models.CharField(max_length=255, default=None)

class D_Date(models.Model):
    code_PK = models.DateField(default='1900-01-01', primary_key=True, unique=True)

class F_Dose(models.Model):
    # pk = vaccine_type_FK + geo_FK + date_FK
    code_PK = models.CharField(max_length=255, default=None, primary_key=True, unique=True)
    vaccine_type_FK = models.ForeignKey(D_Vaccine_Type, max_length=255, default=None,on_delete=models.CASCADE)
    geo_FK = models.ForeignKey(D_Geo, max_length=255, default=None,on_delete=models.CASCADE)
    date_FK = models.ForeignKey(D_Date, default='1900-01-01',on_delete=models.CASCADE)
    count_dose = models.FloatField(null=True, default=None)
    count_ucd = models.FloatField(null=True, default=None)


