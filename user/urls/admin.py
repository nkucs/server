from django.conf.urls import url
from user.views.admin import CreateRoleAPI, GetRoleAPI
from user.views.admin import GetRoleListAPI, DeleteRoleAPI, ModifyRoleAPI

urlpatterns = [
    url(r'create_role?$', CreateRoleAPI.as_view(), name="create_role"),
    url(r'modify_role?$', ModifyRoleAPI.as_view(), name="modify_role"),
    url(r'role_detail?$', GetRoleAPI.as_view(), name="get_role"),
    url(r'role_list?$', GetRoleListAPI.as_view(), name="get_role_list"),
    url(r'role_delete?$', DeleteRoleAPI.as_view(), name="delete_role"),
]
