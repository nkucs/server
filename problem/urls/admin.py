from django.conf.urls import url
from django.urls import path
from ..views.admin import GetProblemAPI,GetProblemsAPI,GetSubmissionsAPI,CreateProblemAPI,EditProblemAPI,DeleteProblemAPI,AddTagAPI

urlpatterns = [
    url(r"get-problem/?$", GetProblemAPI.as_view(), name="get-problem"),
    url(r"get-all-submissions/?$", GetSubmissionsAPI.as_view(), name="get-all-submissions"),
    url(r"create-problem/?$", CreateProblemAPI.as_view(), name="create-problem"),
    url(r"edit-problem/?$", EditProblemAPI.as_view(), name="edit-problem"),
    url(r"delete-problem/?$", DeleteProblemAPI.as_view(), name="delete-problem"),
    url(r"add-tag/?$",AddTagAPI.as_view(),name="add-tag"),
    url(r'get-all-problems/?$', GetProblemsAPI.as_view(), name='get-all-problems'),
]
