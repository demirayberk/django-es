
from dataclasses import asdict

from drf_yasg.utils import swagger_auto_schema  # pyright: ignore
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.mixins.view_validation import ValidateMixin
from api.serializers import ESSearchResponseSchema, SearchSchema
from es.hostname_ip import HostIpSearch


class SearchView(APIView, ValidateMixin):
    """View uses custom authentication"""

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=SearchSchema,
        operation_description="Search Endpoint, authenticate with the token you recieved please",
        responses={
            200: ESSearchResponseSchema,
            403: "Invalid credentials.",
        },
        security=[{"CustomTokenAuth": []}],
    )
    def post(self, request: Request) -> Response:

        search = self._validate_serializer(
            SearchSchema, request.data
        )
        query = search.validated_data["query"]
        es_search = HostIpSearch().search_wildcard(field="Hostname", value=query)
        data = {
            "total": es_search.total,
            "hits": [asdict(hit) for hit in es_search.hits]
        }
        sch = self._validate_serializer(ESSearchResponseSchema, data)
        return Response(
            sch.validated_data
        )
