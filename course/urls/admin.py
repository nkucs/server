from django.conf.urls import url
from course.views.admin import DeleteCourseAPI
from course.views.admin import DuplicateCourseAPI
from course.views.admin import GetAllCourseAPI
from course.views.admin import GetMyCourseAPI
from course.views.admin import AddCourseAPI
from course.views.admin import UpdateAPI
from course.views.admin import GetCourseDetailsAPI


urlpatterns = [
    url(r"get-all-course/?$", GetAllCourseAPI.as_view(), name="get-all-course"),
    url(r"get-my-course/?$", GetMyCourseAPI.as_view(), name="get-my-course"),
    url(r"^delete-course/?$", DeleteCourseAPI.as_view(), name="delete-course"),
    url(r"^duplicate-course/?$", DuplicateCourseAPI.as_view(), name="duplicate-course"),
    url(r"add-course/?$", AddCourseAPI.as_view(), name="add-course"),
    url(r"update-course/?$", UpdateAPI.as_view(), name="update-course"),
    url(r"^get-course-details/?$", GetCourseDetailsAPI.as_view(), name="get-course-details"),
]
