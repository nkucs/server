from django.conf.urls import url
from user.views.admin import CreateRoleAPI, GetRoleAPI
from user.views.admin import GetRoleListAPI, DeleteRoleAPI

urlpatterns = [
    url(r'create_role/?$', CreateRoleAPI.as_view(), name="create_role"),
    url(r'role_detail?$', GetRoleAPI.as_view(), name="get-role"),
    url(r'role_list?$', GetRoleListAPI.as_view(), name="get-role-list"),
    url(r'role_delete?$', DeleteRoleAPI.as_view(), name="delete_role"),
]
