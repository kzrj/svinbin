# # -*- coding: utf-8 -*-
from rest_framework import permissions


class ObjAndUserSameLocationPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method == 'POST':
            return True
        elif request.method == 'PATCH':
            return request.user.is_staff
        elif request.method == 'DELETE':
            return request.user.is_staff
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        elif request.method == 'POST':
            if request.user.is_staff:
                return True
            return obj.location.get_workshop == request.user.employee.workshop

        elif request.method == 'PATCH': 
            return request.user.is_staff

        elif request.method == 'DELETE':
            return request.user.is_staff
        return False


# class SowAndUserSameLocationPermissions(permissions.BasePermission):

#     def has_permission(self, request, view):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         elif request.method == 'POST':
#             if not request.user.employee:
#                 return False


#         elif request.method == 'PATCH':
#             return request.user.is_staff
#         elif request.method == 'DELETE':
#             return request.user.is_staff
#         return False

#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True

#         elif request.method == 'POST':
#             if request.user.is_staff:
#                 return True

#             if obj.location.get_workshop in [1,2] and request.user.employee.workshop in [1,2]:
#                 return True

#             return obj.location.get_workshop == request.user.employee.workshop

#         elif request.method == 'PATCH': 
#             return request.user.is_staff

#         elif request.method == 'DELETE':
#             return request.user.is_staff
#         return False

class WS3Permissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        elif request.method == 'POST':
            if request.user.is_staff:
                return True
            return request.user.employee.workshop.number == 3

        elif request.method == 'PATCH':
            return request.user.is_staff

        elif request.method == 'DELETE':
            return request.user.is_staff

        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method == 'POST':
            if request.user.is_staff:
                return request.user.is_staff
            return request.user.employee.workshop.number == 3

        elif request.method == 'PATCH': 
            return request.user.is_staff
        elif request.method == 'DELETE':
            return request.user.is_staff
        return False


class WS12Permissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        elif request.method == 'POST':
            if request.user.is_staff:
                return True
            if not hasattr(request.user, 'employee'):
                return False
            return request.user.employee.workshop.number in [1, 2]

        elif request.method == 'PATCH':
            return request.user.is_staff

        elif request.method == 'DELETE':
            return request.user.is_staff

        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method == 'POST':
            if request.user.is_staff:
                return True
            if not hasattr(request.user, 'employee'):
                return False
            return request.user.employee.workshop.number in [1, 2]

        elif request.method == 'PATCH': 
            return request.user.is_staff
        elif request.method == 'DELETE':
            return request.user.is_staff
        return False


class ReadOrAdminOnlyPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if request.user.is_staff:
                return True
            else:
                return False
        
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if request.user.is_staff:
                return True
            else:
                return False
