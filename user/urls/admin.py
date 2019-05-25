from django.conf.urls import url
from user.views.admin import GetRoleAPI

urlpatterns = [
    url(r'role_detail?$', GetRoleAPI.as_view(), name="get-role"),
]
