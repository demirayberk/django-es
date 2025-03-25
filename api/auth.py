from typing import NewType, Optional, Text, Tuple

from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from typing_extensions import TypeGuard

from api.mixins.auth import AuthMixin
from core.settings import AUTH_SIGNATURE

User = get_user_model()

AuthHeader = NewType("AuthHeader", Text)


class CustomTokenAuthentication(BaseAuthentication, AuthMixin):
    """Custom token authentication for DRF."""

    def __validate_auth_header(
        self, auth_header: Optional[Text]
    ) -> TypeGuard[AuthHeader]:

        if not auth_header:
            return False

        if not auth_header.startswith(AUTH_SIGNATURE):
            raise AuthenticationFailed("Bad auth Signature")

        if len(auth_header.split()) < 2:
            return False

        return True

    def authenticate(
        self, request: HttpRequest
    ) -> Optional[Tuple[AbstractBaseUser, None]]:
        """Custom auth"""
        auth_header = request.headers.get("Authorization")

        if not self.__validate_auth_header(auth_header):
            return None

        token = auth_header.split(AUTH_SIGNATURE, maxsplit=1)[-1]
        token = token.strip()
        user = self._validate_token(token)

        return (user, None)
