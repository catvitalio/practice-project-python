from rest_framework import permissions

from apps.eats.models import Place


class PlacePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS or
            obj.owner == request.user
        )


class DishPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST' and request.user.is_authenticated:
            owner = Place.objects.values_list(
                'owner', flat=True).get(id=request.data['place'])
            return request.user.id == owner
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS or
            obj.place.owner == request.user
        )
