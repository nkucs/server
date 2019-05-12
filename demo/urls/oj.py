from django.conf.urls import url

from ..views.oj import DemoAPI

urlpatterns = [
    url(r"^demo/?$", DemoAPI.as_view(), name="demo_content_api"),
]