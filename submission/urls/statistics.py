from django.conf.urls import url
from ..views.statistics import GetSubmissionStatAPI

urlpatterns = [
    url(r"^get_submission_stat/?$", GetSubmissionStatAPI.as_view(), name="get_submission_stat"),
]
