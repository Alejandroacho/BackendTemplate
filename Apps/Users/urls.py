from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from Users.views import ProfileViewSet
from Users.views import UserViewSet


router: DefaultRouter = DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register("profiles", ProfileViewSet, basename="profiles")

urlpatterns: list = [
    path("", include(router.urls)),
]
