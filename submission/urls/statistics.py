from django.conf.urls import url

from ..views.statistics import (
    GetACSubmissionRuntimes, GetSubmissionCountAPI, CaseTagStatisticsView,
    GetSubmissionDistributionAPI, GetSubmissionInfoAPI, GetSubmissionStatAPI,
    GetSubmissionTags, GetWordCloud,
    GetProblemSubmissionTags, GetProblemSubmissionCountAPI)

urlpatterns = [
    url(r"^get_submission_stat/?$", GetSubmissionStatAPI.as_view(),
        name="get_submission_stat"),
    url(r"^get-wordcloud/?$", GetWordCloud.as_view(), name="get-wordcloud"),
    url(r"get-submission_count/?$", GetSubmissionCountAPI.as_view(),
        name="get-submission_count"),
    url(r"get_submission_tags/?$", GetSubmissionTags.as_view(),
        name="get_submission_tags"),
    url(r"get_submission_info/?$", GetSubmissionInfoAPI.as_view(),
        name="get_submission_info"),
    url(r"get-all-distribution/?$", GetSubmissionDistributionAPI.as_view(),
        name="get-all-distribution"),
    url(r"get-runtime-ratio/?$", GetACSubmissionRuntimes.as_view(),
        name="get-runtime-ratio"),
    url(r"get-tags-statistics/?$", CaseTagStatisticsView.as_view(),
        name="get-tags-statistics"),
    url(r"get_problem_submission_tag/?$", GetProblemSubmissionTags.as_view(),
        name="get_problem_submission_tag"),
    url(r"get_problem_submission_count/?$", GetProblemSubmissionCountAPI.as_view(),
        name="get_problem_submission_count"),
]
