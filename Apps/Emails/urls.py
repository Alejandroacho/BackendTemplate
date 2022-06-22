from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from Emails.views import SuggestionViewSet


router: DefaultRouter = DefaultRouter()
router.register("suggestions", SuggestionViewSet, basename="users")

urlpatterns: list = [
    path("", include(router.urls)),
]
