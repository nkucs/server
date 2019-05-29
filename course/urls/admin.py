from django.conf.urls import url
from course.views.admin import DeleteCourseAPI
from course.views.admin import DuplicateCourseAPI


from course.views.admin import GetAllCourseAPI
from course.views.admin import GetMyCourseAPI

urlpatterns = [
    url(r"get-all-course/?$", GetAllCourseAPI.as_view(), name="get-all-course"),
    url(r"get-my-course/?$", GetMyCourseAPI.as_view(), name="get-my-course")
    url(r"^delete-course/?$", DeleteCourseAPI.as_view(), name="delete-course"),
    url(r"^duplicate-course/?$", DuplicateCourseAPI.as_view(), name="duplicate-course"),
]
