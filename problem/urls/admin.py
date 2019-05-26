from django.conf.urls import url
from problem.views.admin import CreateProblemAPI,DeleteProblemAPI,EditProblemAPI,AddTagAPI
urlpatterns = [
    url(r"create-problem/?$", CreateProblemAPI.as_view(), name="create-problem"),
    url(r"edit-problem/?$", EditProblemAPI.as_view(), name="edit-problem"),
    url(r"delete-problem/?$", DeleteProblemAPI.as_view(), name="delete-problem"),
    url(r"add-tag/?$",AddTagAPI.as_view(),name="add-tag"),
]