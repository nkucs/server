from django.conf.urls import url
from django.urls import path
from ..views.admin import GetProblemAPI

urlpatterns = [
    url(r"get-problem/?$", GetProblemAPI.as_view(), name="get-problem"),
]