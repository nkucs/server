from django.conf.urls import url
from user.views.admin import CreateRoleAPI, GetRoleAPI, GetRoleTeacherListAPI,\
        GetRoleAddTeacherListAPI, CreateStudentAPI,\
        GetStudentAPI, UpdateStudentAPI, RoleTeacherAddAPI,\
        RoleTeacherDeleteAPI, GetRoleListAPI, DeleteRoleAPI, ModifyRoleAPI

urlpatterns = [
    url(r'create_role?$', CreateRoleAPI.as_view(), name="create_role"),
    url(r'modify_role?$', ModifyRoleAPI.as_view(), name="modify_role"),
    url(r'role_detail?$', GetRoleAPI.as_view(), name="get_role"),
    url(r'role_list?$', GetRoleListAPI.as_view(), name="get_role_list"),
    url(r'role_delete?$', DeleteRoleAPI.as_view(), name="delete_role"),
    url(r'role-teacher-list/?$', GetRoleTeacherListAPI.as_view(), name="role-teacher-list"),
    url(r'role-add-teacher-list/?$', GetRoleAddTeacherListAPI.as_view(), name="role-add-teacher-list"),
    url(r'role-teacher-add/?$', RoleTeacherAddAPI.as_view(), name="role-teacher-add"),
    url(r'role-teacher-delete/?$', RoleTeacherDeleteAPI.as_view(), name="role-teacher-delete"),
    url(r'student_create/?$', CreateStudentAPI.as_view(), name="student_create"),
    url(r'student_get/?$', GetStudentAPI.as_view(), name="student_get"),
    url(r'student_update/?$', UpdateStudentAPI.as_view(), name="student_update"),
]
