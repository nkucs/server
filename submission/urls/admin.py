from django.conf.urls import url

from ..views.admin import GetSubmissionAPI

urlpatterns = [
    url(r"get-submission/?$", GetSubmissionAPI.as_view(), name="get-submission"),
]