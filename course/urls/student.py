from django.conf.urls import url
from course.views.student import GetAllCourseAPI,GetAllMessageAPI,GetMessageOfCourseAPI

urlpatterns = [
    url(r'get-all-course/?$', GetAllCourseAPI.as_view(), name="get-all-course"),
    url(r'get-all-message/?$', GetAllMessageAPI.as_view(), name="get-all-message"),
    url(r'get-course-message/?$', GetMessageOfCourseAPI.as_view(), name="get-course-message"),
]