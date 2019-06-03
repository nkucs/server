from django.conf.urls import url
from course.views.statistics import GetProblemDataAPI,GetTeacherCoursesAPI


urlpatterns = [
    url(r"^problem-data/?$", GetProblemDataAPI.as_view(), name="problem-data"),
    url(r"^get-teacher-courses/?$",GetTeacherCoursesAPI.as_view(),name="get-teacher-courses"),
]