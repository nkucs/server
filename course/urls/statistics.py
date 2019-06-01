from django.conf.urls import url
from course.views.statistics import GetProblemDataAPI


urlpatterns = [
    url(r"^problem-data/?$", GetProblemDataAPI.as_view(), name="problem-data"),
]