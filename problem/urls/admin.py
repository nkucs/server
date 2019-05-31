from django.conf.urls import url
from django.urls import path
from ..views.admin import GetProblemAPI,GetSubmissionsAPI

urlpatterns = [
    url(r"get-problem/?$", GetProblemAPI.as_view(), name="get-problem"),
    url(r"get-all-submissions/?$", GetSubmissionsAPI.as_view(), name="get-all-submissions"),
]
