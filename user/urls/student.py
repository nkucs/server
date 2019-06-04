from django.conf.urls import url
from user.views.student import GetStudentListAPI,DeleteStudentAPI, GetStudentAPI

urlpatterns = [
    url(r'student_list?$', GetStudentListAPI.as_view(), name="get_student_list"),
    url(r'student_delete?$', DeleteStudentAPI.as_view(), name="delete_student"),
    url(r'student_get/?$', GetStudentAPI.as_view(), name="get_student")
    
]