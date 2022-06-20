from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission
from rest_framework.permissions import DjangoObjectPermissions

from Users.models import Profile
from Users.models import User


class IsAdmin(BasePermission):
    message = "You don't have permission"

    def has_permission(self, request, view):
        return request.user.is_admin


class IsVerified(BasePermission):
    message = 'You have to verify your account first'

    def has_permission(self, request, view):
        return request.user.is_verified


class IsUserOwner(BasePermission):
    message = "You don't have permission"

    def has_permission(self, request, view):
        try:
            pk = request.parser_context['kwargs']['pk']
            user = get_object_or_404(User, id=pk)
        except:
            return False
        return request.user.has_permission(user)


class IsSameUserId(BasePermission):
    message = "You don't have permission"

    def has_permission(self, request, view):
        url_user_id = request.GET.get('user_id', request.user.id)
        return request.user.id == int(url_user_id)


class IsProfileOwner(DjangoObjectPermissions):
    message = "You don't have permission"

    def has_permission(self, request, view):
        try:
            pk = request.parser_context['kwargs']['pk']
            profile = get_object_or_404(Profile, id=pk)
        except:
            return False
        return request.user.has_permission(profile)


class IsActionAllowed(DjangoObjectPermissions):
    message = "You don't have permission"
    allowed_actions_for_user = ['retrieve', 'update']

    def has_permission(self, request, view):
        return view.action in self.allowed_actions_for_user
