from django.conf.urls import url
from ..views.student import GetAllSubmissionAPI
from ..views.student import GetUserSubmissionAPI
from ..views.student import AddLabAttachmentAPI

urlpatterns = [
    url(r"get_all_submission/?$", GetAllSubmissionAPI.as_view(), name="get_all_submission"),
    url(r"get_user_submission/?$", GetUserSubmissionAPI.as_view(), name="get_user_submission"),
    url(r"add_ab_attachment/?$", AddLabAttachmentAPI.as_view(), name="add_ab_attachment"),    
]