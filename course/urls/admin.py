from django.conf.urls import url
from course.views.admin import DeleteCourseAPI
from course.views.admin import DuplicateCourseAPI


urlpatterns = [
    url(r"^delete-course/?$", DeleteCourseAPI.as_view(), name="delete-course"),
    url(r"^duplicate-course/?$", DuplicateCourseAPI.as_view(), name="duplicate-course"),
]
