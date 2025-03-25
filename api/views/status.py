from rest_framework.request import Request
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import MessageSchema

class StatusView(APIView):
    """Check the status of the endpoint"""

    def get(self, _: Request) -> Response:
        """Get method for status"""
        sch = MessageSchema({"msg": "App is healthy"})
        return Response(sch.data, status=status.HTTP_200_OK) # pyright: ignore
