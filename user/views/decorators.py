import functools
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
# from rest_framework.permissions import IsAuthenticated
from utils.api import APIView, JSONResponse
from ..models import User, Student, Teacher, Admin

class BasePermissionDecorator(object):
    def __init__(self, func):
        self.func = func
    
    def __get__(self, obj, obj_type):
        return functools.partial(self.__call__, obj)

    def error(self, data):
        return JSONResponse.response({"error": "permission-denied", "msg": data})

    def __call__(self, *args, **kwargs):
        self.request = args[1]

        if self.check_permission():
            if not self.request.user.is_active:
                return self.error("Your account is inactive.")
            return self.func(*args, **kwargs)
        else:
            return self.error("Please login")

    def check_permission(self):
        raise NotImplementedError()

class login_required(BasePermissionDecorator):
    def check_permission(self):
        return self.request.user.is_authenticated()

class admin_required(BasePermissionDecorator):
    @login_required
    def check_permission(self):
        user = self.request.user
        admin_query = Admin.objects.filter(user=user)
        return admin_query.exists()

class stu_required(BasePermissionDecorator):
    @login_required
    def check_permission(self):
        user = self.request.user
        stu_query = Student.objects.filter(user=user)
        return stu_query.exists()

class teach_required(BasePermissionDecorator):
    @login_required
    def check_permission(self):
        user = self.request.user
        teach_query = Teacher.objects.filter(user=user)
        return teach_query.exists()

