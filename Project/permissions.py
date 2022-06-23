from django.http import HttpRequest
from django.views import View
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission
from rest_framework.permissions import DjangoObjectPermissions
from Users.models import Profile
from Users.models import User


class IsAdmin(BasePermission):
    message: str = "You don't have permission"

    def has_permission(self, request: HttpRequest, view: View) -> bool:
        return request.user.is_admin


class IsVerified(BasePermission):
    message: str = "You have to verify your account first"

    def has_permission(self, request: HttpRequest, view: View) -> bool:
        return request.user.is_verified


class IsUserOwner(BasePermission):
    message: str = "You don't have permission"

    def has_permission(self, request: HttpRequest, view: View) -> bool:
        try:
            pk: int = request.parser_context["kwargs"]["pk"]
            user: User = get_object_or_404(User, id=pk)
        except:
            return False
        return request.user.has_permission(user)


class IsSameUserId(BasePermission):
    message: str = "You don't have permission"

    def has_permission(self, request: HttpRequest, view: View) -> bool:
        url_user_id: int = request.GET.get("user_id", request.user.id)
        return request.user.id == int(url_user_id)


class IsProfileOwner(DjangoObjectPermissions):
    message: str = "You don't have permission"

    def has_permission(self, request: HttpRequest, view: View) -> bool:
        try:
            pk: int = request.parser_context["kwargs"]["pk"]
            profile: Profile = get_object_or_404(Profile, id=pk)
        except:
            return False
        return request.user.has_permission(profile)


class IsActionAllowed(DjangoObjectPermissions):
    message: str = "You don't have permission"
    allowed_actions_for_user: list = ["retrieve", "update"]

    def has_permission(self, request: HttpRequest, view: View) -> bool:
        return view.action in self.allowed_actions_for_user
