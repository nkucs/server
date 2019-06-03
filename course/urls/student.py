from django.conf.urls import url
from django.urls import path
from course.views.student import GetCourseAPI

urlpatterns = [
    url(r"student-personal-information/?$", GetCourseAPI.as_view(), name="student-personal-information"),
]