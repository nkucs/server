from django.conf.urls import url
from ..views.student import LabAPI, LabDetailAPI

urlpatterns = [
    url(r"^lab_course_list/?$", LabAPI.as_view(), name="lab_list_api"),
    url(r"^lab_course_detail/?$", LabDetailAPI.as_view(), name="lab_detail_api")
]