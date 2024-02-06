# from rest_framework.permissions import BasePermission, SAFE_METHODS
# #
# #
# # class IsSuperUser(BasePermission):
# #
# #     def has_permission(self, request, view):
# #         return request.method='',bool(request.user and request.user.is_authenticated and request.user.is_superuser)
# #
#
# from rest_framework.permissions import BasePermission
#
#
# class IsSuperUser(BasePermission):
#     def has_permission(self, request, view):
#         return request.method == 'POST' and request.user and request.user.is_superuser
