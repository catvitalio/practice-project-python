from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions
from rest_framework.exceptions import APIException

from apps.eats.models import Place


class PlacePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
                request.method in permissions.SAFE_METHODS or
                request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
                request.method in permissions.SAFE_METHODS or
                obj.owner == request.user
        )


class DishPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST' and request.user.is_authenticated:
            try:
                owner = Place.objects.get(id=request.data['place']).owner
                return request.user == owner
            except ObjectDoesNotExist:
                raise APIException("Выбранного заведения нет в списке")
            except KeyError:
                raise APIException("Заведение не выбрано")

        return (
                request.method in permissions.SAFE_METHODS or
                request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
                request.method in permissions.SAFE_METHODS or
                obj.place.owner == request.user
        )
