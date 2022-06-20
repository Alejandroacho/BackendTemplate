from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from App.pagination import ListResultsSetPagination
from App.permissions import IsAdmin
from App.permissions import IsSameUserId
from App.permissions import IsVerified
from Emails.factories.suggestion import (
    SuggestionEmailFactory as SuggestionEmail,
)
from Emails.models.models import Suggestion
from Emails.serializers import SuggestionEmailSerializer
from Users.models import User


CREATED = status.HTTP_201_CREATED


class SuggestionViewSet(viewsets.GenericViewSet):
    """
    API endpoint that allows users to create and list suggestions email.
    Allows also to admins to mark a suggestions as read.
    """

    SUBMIT_PERMISSIONS = [IsAuthenticated & IsVerified]
    LIST_PERMISSIONS = [IsAuthenticated & (IsAdmin | IsSameUserId)]
    READ_PERMISSIONS = [IsAuthenticated & IsAdmin]
    queryset = Suggestion.objects.all().order_by('-id')
    pagination_class = ListResultsSetPagination

    @action(
        detail=False, methods=['post'], permission_classes=SUBMIT_PERMISSIONS
    )
    def submit(self, request):
        type = request.data.get('type')
        content = request.data.get('content')
        user = User.objects.get(id=request.user.id)
        suggestion = SuggestionEmail(type=type, content=content, user=user)
        suggestion.send()
        data = SuggestionEmailSerializer(suggestion).data
        return Response(data=data, status=CREATED)

    @action(detail=True, methods=['post'], permission_classes=READ_PERMISSIONS)
    def read(self, request, pk=None):
        suggestion = get_object_or_404(Suggestion, pk=pk)
        suggestion.was_read = True
        suggestion.save()
        data = SuggestionEmailSerializer(suggestion).data
        return Response(data=data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], permission_classes=LIST_PERMISSIONS)
    def user(self, request):
        user_id = request.GET.get('user_id', request.user.id)
        suggestions = self.queryset.filter(user_id=user_id)
        page = self.paginate_queryset(suggestions)
        data = SuggestionEmailSerializer(page, many=True).data
        return self.get_paginated_response(data)
