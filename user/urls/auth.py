from django.urls import re_path
from user.views.admin import UserAuthAPI

# usertype = ['stud', 'teac', 'admi']
urlpatterns = [
    re_path(r'(?P<usertype>[a-z]{4})login?$', UserAuthAPI.as_view(), name="login"),
]
