from django.conf.urls import url
from django.urls import path
from ..views.admin import GetLabsAPI, GetSubmissionFileAPI, GetLabAPI

urlpatterns = [
    url(r"get-my-labs/?$", GetLabsAPI.as_view(), name="get-my-labs"),
    path('get-submission-file/', GetSubmissionFileAPI.as_view(), name='get-submission-file'),
    path('get-lab/', GetLabAPI.as_view(), name='get-lab'),
]
