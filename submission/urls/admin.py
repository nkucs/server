from django.conf.urls import url

from ..views.admin import GetSubmissionAPI,GetSubmissionsAPI

urlpatterns = [
    url(r"get-submission/?$", GetSubmissionAPI.as_view(), name="get-submission"),
    url(r"get-all-submissions/?$", GetSubmissionsAPI.as_view(), name="get-all-submissions"),
]
