from django.conf.urls import url

from ..views.admin import GetLabsAPI

urlpatterns = [
    url(r"get-my-labs/?$", GetLabsAPI.as_view(), name="get-my-labs"),
]
