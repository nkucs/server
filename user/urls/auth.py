from django.conf.urls import url
from django.urls import re_path
from user.views.admin import UserLoginAPI, UserLogoutAPI

# usertype = ['stud', 'teac', 'admi']
urlpatterns = [
    re_path(r'(?P<usertype>[a-z]{4})login?$', UserLoginAPI.as_view(), name="login"),
    url(r'logout?$', UserLogoutAPI.as_view(), name="logout")
]
