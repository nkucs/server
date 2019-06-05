from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Group
from .models import Permission

def getPermission(request, index):
    user = request.user
    groups = Group.objects.filter(user=user)
    permissionNeeded = Permission.objects.get(id=index)
    for group in groups:
        permissions = group.role.permission.all()
        for permission in permissions:
            if permission == permissionNeeded:
                return True
    return False


class ManageTeacherPermission(BasePermission):
    """
    教师管理权限
    """

    def has_permission(self, request, view):
        if(getPermission(request, 1)):
            return True
        return False


class ManageStudentPermission(BasePermission):
    """
    学生管理权限
    """

    def has_permission(self, request, view):
        if(getPermission(request, 2)):
            return True
        return False


class ManageCoursePermission(BasePermission):
    """
    课程系列管理权限
    """

    def has_permission(self, request, view):
        if(getPermission(request, 3)):
            return True
        return False


class ManageClassPermission(BasePermission):
    """
    课程管理权限
    """

    def has_permission(self, request, view):
        if(getPermission(request, 4)):
            return True
        return False


class ManageExamPermission(BasePermission):
    """
    考试管理权限
    """

    def has_permission(self, request, view):
        if(getPermission(request, 5)):
            return True
        return False


class ManageExamCodePermission(BasePermission):
    """
    考试密码管理权限
    """

    def has_permission(self, request, view):
        if(getPermission(request, 6)):
            return True
        return False


class ManageMessagePermission(BasePermission):
    """
    消息管理权限
    """

    def has_permission(self, request, view):
        if(getPermission(request, 7)):
            return True
        return False


class ManageProgrammingTopicPermission(BasePermission):
    """
    编程题目管理权限
    """

    def has_permission(self, request, view):
        if(getPermission(request, 8)):
            return True
        return False


class ManageLabelPermission(BasePermission):
    """
    标签管理权限
    """

    def has_permission(self, request, view):
        if(getPermission(request, 9)):
            return True
        return False


class ManageReportTopicPermission(BasePermission):
    """
    报告题目管理权限
    """

    def has_permission(self, request, view):
        if(getPermission(request, 10)):
            return True
        return False


class ManageCourseResourcesPermission(BasePermission):
    """
    课程资源管理权限
    """

    def has_permission(self, request, view):
        if(getPermission(request, 11)):
            return True
        return False


class ManageExperimentPermission(BasePermission):
    """
    实验题目管理权限
    """

    def has_permission(self, request, view):
        if(getPermission(request, 12)):
            return True
        return False


class ManageAccessPermission(BasePermission):
    """
    权限管理权限
    """

    def has_permission(self, request, view):
        if(getPermission(request, 13)):
            return True
        return False


class ManageRolePermission(BasePermission):
    """
    角色管理权限
    """

    def has_permission(self, request, view):
        if(getPermission(request, 14)):
            return True
        return False
