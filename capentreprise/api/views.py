from rest_framework.pagination import PageNumberPagination

from data_parser.models import F_Dose, D_Date, D_Geo, D_Vaccine_Type
from api.serializers import F_Dose_Serializer, D_Date_Serializer, D_Geo_Serializer, D_Vaccine_Type_Serializer

from capentreprise.settings import DATABASES

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class DWH_api(APIView):
    """My first API

    Args:
        APIView (_type_): _description_
    """

    lookup_field = 'code_PK'

    def get(self, request, code_PK=None):

        if code_PK is not None and 'table' in request.GET:
            flag = False
            table_name = request.GET['table']
            count = 1
            data = eval(table_name).objects.filter(code_PK=code_PK)
            serializer = eval(f"{table_name}_Serializer")(data=data, many=True)


        else:
            flag = True
            if 'table' in request.GET:
                table_name = request.GET['table']
                data = eval(table_name).objects.all()
                count = data.count()
                paginator = PageNumberPagination()
                paginator.page_size = 5
                paginated_queryset = paginator.paginate_queryset(data, request)
                serializer = eval(f"{table_name}_Serializer")(data=paginated_queryset, many=True)

            else:
                table_name = 'F_Dose'
                data = F_Dose.objects.all()
                count = data.count()
                paginator = PageNumberPagination()
                paginator.page_size = 5
                paginated_queryset = paginator.paginate_queryset(data, request)
                serializer = eval(f"{table_name}_Serializer")(data=paginated_queryset, many=True)

        serializer.is_valid()
        data = serializer.data

        result = {
                'home': 'http://localhost:8000/',
                'table_name': table_name,
                'Nombre de ligne': count,
                'data': data,
                'next': paginator.get_next_link(),
                'previous': paginator.get_previous_link()
            }

        return Response(result, status=status.HTTP_200_OK)


