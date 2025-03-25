import base64
import hashlib
import secrets
from typing import Optional, Text

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from rest_framework.exceptions import AuthenticationFailed
from core.settings import SECRET_KEY

User = get_user_model()


class AuthMixin:

    def _generate_token(self, username: Text) -> Text:
        """
        Generates a simple token by combining username with secret key,
        then base64 encoding it.
        """
        token_data = username + SECRET_KEY
        token_hash = hashlib.sha256(token_data.encode("utf-8")).hexdigest()

        token_content = f"{username}:{token_hash}"
        token = base64.b64encode(token_content.encode("utf-8")).decode("utf-8")

        return token

    def _validate_token(self, token: Optional[Text]) -> AbstractBaseUser:
        """
        Validates the token and returns the corresponding user.
        """
        if not token:
            raise AuthenticationFailed("Please provide a token")

        try:
            decoded_token = base64.b64decode(token.encode("utf-8")).decode("utf-8")
            username, _ = decoded_token.split(":", maxsplit=1)

            if not secrets.compare_digest(token, self._generate_token(username)):
                raise AuthenticationFailed("Invalid token")

            # Get user
            user = User.objects.get(username=username)

        except (UnicodeDecodeError, ValueError) as exc:
            raise AuthenticationFailed("Invalid token format") from exc
        except User.DoesNotExist as exc:
            raise AuthenticationFailed("User not found") from exc

        return user
