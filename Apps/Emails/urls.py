from django.urls import include
from django.urls import path
from Emails.views import SuggestionViewSet
from rest_framework.routers import DefaultRouter


router: DefaultRouter = DefaultRouter()
router.register("suggestions", SuggestionViewSet, basename="users")

urlpatterns: list = [
    path("", include(router.urls)),
]
