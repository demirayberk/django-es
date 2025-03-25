from django.urls import path, include

from api.views import CreateUserView, LoginView, SearchView, StatusView

urlpatterns = [
    path("status/", StatusView().as_view(), name="status"),
    path("search/", SearchView().as_view(), name="search"),
    path(
        "auth/",
        include(
            [
                path("token/", LoginView.as_view(), name="login"),
                path(
                    "register/", CreateUserView.as_view(), name="register"
                ),
            ]
        ),
    ),
]
