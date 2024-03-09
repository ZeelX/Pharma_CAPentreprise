from rest_framework.pagination import PageNumberPagination
from capentreprise.settings import LOGIN_URL
from data_parser.models import F_Dose, D_Date, D_Geo, D_Vaccine_Type
from api.serializers import F_Dose_Serializer, D_Date_Serializer, D_Geo_Serializer, D_Vaccine_Type_Serializer

from capentreprise.settings import DATABASES

from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required


# @login_required(login_url=LOGIN_URL)
class DWH_api(APIView):
    """Api for fetching data from the database


    Args:
        APIView (_type_): _description_
        code_pk = string
        all table use same name for their pk
    """
    # block access to API without credential

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    lookup_field = 'code_PK'

    def get(self, request, code_PK=None):
        headers_token = request.headers.get('Authorization')
        if code_PK is not None and 'table' in request.GET:
            table_name = request.GET['table']
            data = eval(table_name).objects.filter(code_PK=code_PK)
            serializer = eval(f"{table_name}_Serializer")(data=data, many=True)

            serializer.is_valid()
            data = serializer.data

            result = {
                'home': 'http://localhost:8000/',
                'table_name': table_name,
                'Nombre de ligne': 1,
                'data': data,
            }



        else:
            if 'table' in request.GET:
                table_name = request.GET['table']
                data = eval(table_name).objects.all()
                flag = True


            else:
                table_name = 'F_Dose'
                data = F_Dose.objects.all()
                flag = False

            count = data.count()
            paginator = PageNumberPagination()
            paginator.page_size = 5
            paginated_queryset = paginator.paginate_queryset(data, request)
            if flag:
                serializer = eval(f"{table_name}_Serializer")(data=paginated_queryset, many=True)
            else:
                serializer = F_Dose_Serializer(data=paginated_queryset, many=True)

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

    def post(self, request):
        if 'table' in request.GET:
            flag = False
            table_name = request.GET['table']
            data = request.data
            serializer = eval(f"{table_name}_Serializer")(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'message': "You need to add a table on your request to do that"},
                            status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, code_PK=None):
        """_summary_
        """

        if 'table' in request.GET:
            table_name = request.GET['table']
            queryset = table_name.objects.filter(code_PK=code_PK).first()

            if queryset is not None:
                serializer = eval(f"{table_name}_Serializer")(queryset, request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(data=serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response(data={'message': f"object {table_name} referenced by {code_PK} was not found."},
                                status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(data={'message': "You need to add a table on your request to do that"},
                            status=status.HTTP_400_BAD_REQUEST)
