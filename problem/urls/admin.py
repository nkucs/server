from django.conf.urls import url
from django.urls import path
from ..views.admin import GetProblemAPI, GetProblemsAPI

urlpatterns = [
    url(r"get-problem/?$", GetProblemAPI.as_view(), name="get-problem"),
    url(r'get-all-problems/?$', GetProblemsAPI.as_view(), name='get-all-problems'),
]