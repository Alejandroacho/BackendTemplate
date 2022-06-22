from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Project.pagination import ListResultsSetPagination
from Project.permissions import IsAdmin
from Project.permissions import IsSameUserId
from Project.permissions import IsVerified
from Emails.factories.suggestion import SuggestionEmailFactory
from Emails.models.models import Suggestion
from Emails.serializers import SuggestionEmailSerializer
from Users.models import User


CREATED = status.HTTP_201_CREATED


class SuggestionViewSet(viewsets.GenericViewSet):
    """
    API endpoint that allows users to create and list suggestions email.
    Allows also to admins to mark a suggestions as read.
    """

    SUBMIT_PERMISSIONS: list = [IsAuthenticated & IsVerified]
    LIST_PERMISSIONS: list = [IsAuthenticated & (IsAdmin | IsSameUserId)]
    READ_PERMISSIONS: list = [IsAuthenticated & IsAdmin]
    queryset: QuerySet = Suggestion.objects.all().order_by("-id")
    pagination_class: PageNumberPagination = ListResultsSetPagination

    @action(
        detail=False, methods=["post"], permission_classes=SUBMIT_PERMISSIONS
    )
    def submit(self, request: HttpRequest) -> Response:
        type: str = request.data.get("type")
        content: str = request.data.get("content")
        user: User = User.objects.get(id=request.user.id)
        suggestion: Suggestion = SuggestionEmailFactory(
            type=type, content=content, user=user
        )
        suggestion.send()
        data = SuggestionEmailSerializer(suggestion).data
        return Response(data=data, status=CREATED)

    @action(detail=True, methods=["post"], permission_classes=READ_PERMISSIONS)
    def read(self, request: HttpRequest, pk: int = None) -> Response:
        suggestion: Suggestion = get_object_or_404(Suggestion, pk=pk)
        suggestion.was_read = True
        suggestion.save()
        data: dict = SuggestionEmailSerializer(suggestion).data
        return Response(data=data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], permission_classes=LIST_PERMISSIONS)
    def user(self, request: HttpRequest) -> Response:
        user_id: int = request.GET.get("user_id", request.user.id)
        suggestions: QuerySet = self.queryset.filter(user_id=user_id)
        page: QuerySet = self.paginate_queryset(suggestions)
        data: dict = SuggestionEmailSerializer(page, many=True).data
        return self.get_paginated_response(data)
