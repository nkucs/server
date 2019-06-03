from django.conf.urls import url
from course.views.student import GetAllCourseAPI

urlpatterns = [
    url(r'get-all-course/?$', GetAllCourseAPI.as_view(), name="get-all-course"),
]