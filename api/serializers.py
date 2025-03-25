from typing import Any, Text, TypedDict, Dict

from django.http import QueryDict
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


class SearchSchema(serializers.Serializer[QueryDict]):
    """Serializer for search endpoint"""

    query = serializers.CharField(required=True)

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

class ESSearchResponseSchema(serializers.Serializer[Dict[Text, Any]]):
    total = serializers.IntegerField()
    hits = HostIPSchema(many=True)
