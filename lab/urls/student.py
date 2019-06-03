from django.conf.urls import url
from ..views.student import LabAPI, LabDetailAPI
from ..views.student import ProblemHandInAPI
from ..views.student import TestDetailAPI

from ..views.student import LabAPI, LabDetailAPI, PostAttachmentAPI

urlpatterns = [
    url(r"^lab_course_list/?$", LabAPI.as_view(), name="lab_list_api"),
    url(r"^lab_course_detail/?$", LabDetailAPI.as_view(), name="lab_detail_api"),
    url(r"^problem_hand_in/?$", ProblemHandInAPI.as_view(), name="problem_hand_in_api"),
    url(r"^lab_attachment_hand_in/?$", PostAttachmentAPI.as_view(), name='post-attachment'),
    url(r"^test_detail/?$", TestDetailAPI.as_view(), name='test-detail')
]