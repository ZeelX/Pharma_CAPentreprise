from rest_framework import serializers
from data_parser.models import D_Geo, D_Date, D_Vaccine_Type, F_Dose


class D_Geo_Serializer(serializers.ModelSerializer):
    class Meta:
        model = D_Geo
        fields = '__all__'


class D_Date_Serializer(serializers.ModelSerializer):
    class Meta:
        model = D_Date
        fields = '__all__'


class D_Vaccine_Type_Serializer(serializers.ModelSerializer):
    class Meta:
        model = D_Vaccine_Type
        fields = '__all__'


class F_Dose_Serializer(serializers.ModelSerializer):
    class Meta:
        model = F_Dose
        fields = '__all__'
