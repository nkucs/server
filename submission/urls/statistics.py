from django.conf.urls import url
from ..views.statistics import GetSubmissionStatAPI
from ..views.statistics import GetSubmissionCountAPI
from ..views.statistics import GetWordCloud

urlpatterns = [
    url(r"^get_submission_stat/?$", GetSubmissionStatAPI.as_view(),
        name="get_submission_stat"),
    url(r"^get-wordcloud/?$", GetWordCloud.as_view(), name="get-wordcloud"),
    url(r"get-submission_count/?$", GetSubmissionCountAPI.as_view(),
        name="get-submission_count"),
]