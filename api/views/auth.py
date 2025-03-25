from typing import cast

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from drf_yasg.utils import swagger_auto_schema  # pyright: ignore
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.mixins.auth import AuthMixin
from api.mixins.view_validation import ValidateMixin
from api.serializers import BasicUserSchema, ErrorSchema, TokenCreatedSchema, UserCreatedSchema
from core.settings import MOCK_PASSWORD, MOCK_USERNAME

User = get_user_model()


class LoginView(APIView, ValidateMixin, AuthMixin):
    """Endpoint for login"""

    @swagger_auto_schema(
        request_body=BasicUserSchema,  # Specify the request body schema
        responses={
            200: TokenCreatedSchema,
            401: ErrorSchema,
            403: "Invalid Credentials",
        },
        operation_description=f"Authenticate a user and return a token. You can test with my mock user {MOCK_USERNAME}:{MOCK_PASSWORD}",
    )
    def post(self, request: Request) -> Response:

        login = self._validate_serializer(BasicUserSchema, request.data)
        print(request.data)

        # Proceed with login logic
        username = login.validated_data["username"]
        password = login.validated_data["password"]

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if not user:
            msg = {"error": "Invalid credentials"}
            err = self._validate_serializer(ErrorSchema, msg)
            return Response(err.validated_data, status=status.HTTP_401_UNAUTHORIZED)
        token = self._generate_token(username)
        sch = self._validate_serializer(TokenCreatedSchema, {"token": token})
        return Response(sch.validated_data, status=status.HTTP_200_OK)


class CreateUserView(APIView, ValidateMixin):
    """Endpoint for user registration"""

    @swagger_auto_schema(
        request_body=BasicUserSchema,
        responses={
            201: UserCreatedSchema,
            400: ErrorSchema,
        },
        operation_description="Create a new user account",
    )
    def post(self, request: Request) -> Response:

        register = self._validate_serializer(BasicUserSchema, request.data)
        username = register.validated_data["username"]
        password = register.validated_data["password"]
        if User.objects.filter(username=username).exists():
            msg = {"error": "Username Exists"}
            err = self._validate_serializer(ErrorSchema, msg)
            return Response(
                err.validated_data, status=status.HTTP_400_BAD_REQUEST
            )
        user = User.objects.create_user(  # pyright: ignore
            username=username, password=password
        )
        user = cast(AbstractBaseUser, user)
        msg = {"msg": "User created successfully", "username": user.get_username()}
        sch = self._validate_serializer(UserCreatedSchema, msg)
        return Response(
            sch.validated_data,
            status=status.HTTP_201_CREATED,
        )
