from typing import Any, Dict, Text, TypedDict

from django.http import QueryDict
from django_celery_beat.models import MaxValueValidator
from rest_framework import serializers

#TODO: modularize serializers


class Login(TypedDict):
    """Type declaration for Login"""

    username: str
    password: str


class BasicUserSchema(serializers.Serializer[QueryDict]):
    """Serializer for login endpoint"""

    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class PaginationSchema(serializers.Serializer[Dict[Text, Text]]):

    page = serializers.IntegerField(default=1)
    page_size = serializers.IntegerField(
        required=False,
        default=10,
        validators=[MaxValueValidator(999)]
    )

class SearchSchema(PaginationSchema):
    """Serializer for search endpoint"""
    query = serializers.CharField(default="*")

class ErrorSchema(serializers.Serializer[Dict[Text, Text]]):
    """Errorschema"""
    error = serializers.CharField(default="An Error occured")

class MessageSchema(serializers.Serializer[Dict[Text, Text]]):
    """Errorschema"""
    msg = serializers.CharField(default="Completed")

class UserCreatedSchema(MessageSchema):
    """UserCreatedSchema"""
    username = serializers.CharField(required=True)

class TokenCreatedSchema(MessageSchema):
    """MessageCreatedSchema"""
    token = serializers.CharField(required=True)


class HostIPSchema(serializers.Serializer[Dict[Text, Text]]):
    Hostname = serializers.CharField()
    Ip = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=[],
        help_text="List of IP addresses"
    )

class ESSearchResponseSchema(PaginationSchema):
    total = serializers.IntegerField()
    total_pages = serializers.IntegerField()
    hits = HostIPSchema(many=True)
