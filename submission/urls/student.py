from django.conf.urls import url
from ..views.student import GetAllStudentSubmissionAPI
from ..views.student import GetUserSubmissionAPI
from ..views.student import AddLabAttachmentAPI
from ..views.student import CreateProblemSubmissionAPI
from ..views.student import GetProblemSubmissionAPI

urlpatterns = [
    url(r"get_all_submission/?$", GetAllStudentSubmissionAPI.as_view(), name="get_all_submission"),
    url(r"get_user_submission/?$", GetUserSubmissionAPI.as_view(), name="get_user_submission"),
    url(r"get_problem_submission/?$", GetProblemSubmissionAPI.as_view(), name="get_problem_submission"),
    url(r"add_ab_attachment/?$", AddLabAttachmentAPI.as_view(), name="add_ab_attachment"),    
    url(r"add_problem_submission/?$", CreateProblemSubmissionAPI.as_view(), name="add_problem_submission"),    
]