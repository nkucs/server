from django.conf.urls import url
<<<<<<< HEAD
from ..views.student import LabAPI, LabDetailAPI
from ..views.student import ProblemHandInAPI
=======
from ..views.student import LabAPI, LabDetailAPI, PostAttachmentAPI
>>>>>>> f41b34c98e220c015e90f23b3462ba25de110bd4

urlpatterns = [
    url(r"^lab_course_list/?$", LabAPI.as_view(), name="lab_list_api"),
    url(r"^lab_course_detail/?$", LabDetailAPI.as_view(), name="lab_detail_api"),
    url(r"^problem_hand_in/?$", ProblemHandInAPI.as_view(), name="problem_hand_in_api"),
    url(r"^lab_attachment_hand_in/?$", PostAttachmentAPI.as_view(), name='post-attachment')
]