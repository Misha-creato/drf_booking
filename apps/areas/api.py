from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,

)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import filters

from django_filters import rest_framework

from utils.response_patterns import (
    generate_response,
)

from areas.doc import (
    DefaultAreaResponse,
    AreaList200Response,
    Area200Response,
)
from areas.filters import AreaFilter
from areas.services import (
    get_areas,
    get_area,
)


class AreaListView(APIView):

    filter_backends = [filters.SearchFilter, filters.OrderingFilter, rest_framework.DjangoFilterBackend]
    search_fields = ['name']
    ordering_fields = ['price_int', 'created_at', 'capacity']
    filter_fields = ['price']
    filterset_class = AreaFilter

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='search',
                description='Название площадки',
                required=False,
                type=OpenApiTypes.STR
            ),
        ],
        responses={
            200: AreaList200Response,
            500: DefaultAreaResponse,
        },
        description=AreaList200Response.__doc__,
        summary='Получение списка всех площадок',
    )
    def get(self, request):
        status_code, response_data = get_areas(
            request=request,
            filter_backends=self.filter_backends,
            view=self,
        )
        status, data = generate_response(
            status_code=status_code,
            data=response_data,
        )
        return Response(
            status=status,
            data=data,
        )


class AreaView(APIView):
    @extend_schema(
        responses={
            200: Area200Response,
            404: DefaultAreaResponse,
            500: DefaultAreaResponse,
        },
        description=Area200Response.__doc__,
        summary='Получение площадки по pk',
    )
    def get(self, request, pk):
        status_code, response_data = get_area(
            pk=pk,
        )
        status, data = generate_response(
            status_code=status_code,
            data=response_data,
        )
        return Response(
            status=status,
            data=data,
        )
