from rest_framework import permissions
from rest_framework.compat import is_authenticated

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user ###Если владелец задачи и пользователь равны, то вернуть объект


class IsNotAuthenticated(permissions.BasePermission): ###Не прошел аудентификацию
    def has_permission(self, request, view):
        if request.method == 'POST':
            return not is_authenticated(request.user) or request.user.is_staff  ### если аудентифицирован или  пользователь с особыми правами
        else:
            return request.user.is_staff or False  ### если пользователь с особыми правами

