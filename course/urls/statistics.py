from django.conf.urls import url
from course.views.statistics import GetProblemDataAPI
from course.views.admin import GetMyStudentsAPI
from course.views.admin import GetMyProblemsAPI

urlpatterns = [
    url(r"^problem-data/?$", GetProblemDataAPI.as_view(), name="problem-data"),
    url(r"get-my-students/?$", GetMyStudentsAPI.as_view()),
    url(r"get-my-problems/?$", GetMyProblemsAPI.as_view()),
]