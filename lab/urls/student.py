from django.conf.urls import url
from ..views.student import LabAPI, LabDetailAPI
from ..views.student import ProblemHandInAPI

urlpatterns = [
    url(r"^lab_course_list/?$", LabAPI.as_view(), name="lab_list_api"),
    url(r"^lab_course_detail/?$", LabDetailAPI.as_view(), name="lab_detail_api"),
    url(r"^problem_hand_in/?$", ProblemHandInAPI.as_view(), name="problem_hand_in_api")
]