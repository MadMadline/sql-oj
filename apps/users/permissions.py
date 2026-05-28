from rest_framework.permissions import BasePermission


class IsTeacher(BasePermission):
    """允许教师角色访问"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'teacher'


class IsAdmin(BasePermission):
    """允许管理员角色访问"""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.permission_level == 'admin'
        )


class IsOwnerOrTeacher(BasePermission):
    """只有本人或教师可以访问对象"""
    def has_object_permission(self, request, view, obj):
        return request.user == obj or request.user.user_type == 'teacher'
