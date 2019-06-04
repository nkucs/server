from django.conf.urls import url
from problem.views.student import GetProblemAPI,GetCaseOfProblemAPI

urlpatterns = [
    url(r"get-problem/?$", GetProblemAPI.as_view(), name="get-problem"),
    url(r"get-problem-cases/?$", GetCaseOfProblemAPI.as_view(), name="get-problem-cases"),
]