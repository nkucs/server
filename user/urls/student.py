from django.conf.urls import url
from user.views.student import GetStudentListAPI,DeleteStudentAPI

urlpatterns = [
    url(r'student_list?$', GetStudentListAPI.as_view(), name="get_student_list"),
    url(r'student_delete?$', DeleteStudentAPI.as_view(), name="delete_student")
    
]