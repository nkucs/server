from django.conf.urls import url
from course.views.student import GetAllCourseAPI,GetAllMessageAPI,GetMessageOfCourseAPI,GetMyCourseAPI,GetMyCourseByIDAPI

urlpatterns = [
    url(r'get-all-course/?$', GetAllCourseAPI.as_view(), name="get-all-course"),
    url(r'get-all-message/?$', GetAllMessageAPI.as_view(), name="get-all-message"),
    url(r'get-course-message/?$', GetMessageOfCourseAPI.as_view(), name="get-course-message"),
    url(r'get-my-course/?$',GetMyCourseAPI.as_view(),name="get-my-course"),
    url(r'get-my-course-by-id/?$',GetMyCourseByIDAPI.as_view(),name="get-my-course-by-id")
]