from typing import Any, Dict, Type, TypeVar, Union

from django.http import QueryDict
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

_SR = TypeVar("_SR", bound=serializers.Serializer[Any])


class ValidateMixin:
    """
    A mixin to validate serializers with generic type support.
    """

    def _validate_serializer(
        self, serializer_class: Type[_SR], data: Union[QueryDict, Dict[str, Any]]
    ) -> _SR:
        serializer = serializer_class(data=data)

        # Validate the data
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)  # pyright: ignore

        return serializer
