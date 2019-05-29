from django.conf.urls import url

from course.views.admin import GetAllCourseAPI
from course.views.admin import GetMyCourseAPI

urlpatterns = [
    url(r"get-all-course/?$", GetAllCourseAPI.as_view(), name="get-all-course"),
    url(r"get-my-course/?$", GetMyCourseAPI.as_view(), name="get-my-course")
]
