from django.urls import re_path
from django.conf.urls import url
from user.views.admin import CreateRoleAPI, GetRoleAPI
from user.views.admin import GetRoleListAPI, DeleteRoleAPI, ModifyRoleAPI, UserAuthAPI

user = ['stud', 'teac', 'admi']
urlpatterns = [
    url(r'create_role?$', CreateRoleAPI.as_view(), name="create_role"),
    url(r'modify_role?$', ModifyRoleAPI.as_view(), name="modify_role"),
    url(r'role_detail?$', GetRoleAPI.as_view(), name="get_role"),
    url(r'role_list?$', GetRoleListAPI.as_view(), name="get_role_list"),
    url(r'role_delete?$', DeleteRoleAPI.as_view(), name="delete_role"),
    re_path(r'(?P<usertype>[a-z]{4})login?$', UserAuthAPI.as_view(), name="login")
]
