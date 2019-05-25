from django.conf.urls import url
from user.views.admin import CreateRoleAPI
from user.views.admin import GetRoleAPI, GetRoleListAPI

urlpatterns = [
    url(r'create_role/?$', CreateRoleAPI.as_view(), name="create_role"),
    url(r'role_detail?$', GetRoleAPI.as_view(), name="get-role"),
    url(r'role_list?$', GetRoleListAPI.as_view(), name="get-role-list"),
]
