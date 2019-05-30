from django.conf.urls import url

from exam.views.admin import GetExamStudentAPI
from exam.views.admin import GetIdStudentAPI
from exam.views.admin import GetNameStudentAPI
from exam.views.admin import AddStudentAPI
from exam.views.admin import DeleteStudentAPI

urlpatterns = [
    url(r"get-examstudent/?$", GetExamStudentAPI.as_view(), name="get-examstudent"),
    url(r"get-idstudent/?$", GetIdStudentAPI.as_view(), name="get-idstudent"),
    url(r"get-namestudent/?$", GetNameStudentAPI.as_view(), name="get-namestudent"),
    url(r"add-student/?$", AddStudentAPI.as_view(), name="add-student"),
    url(r"delete-student/?$", DeleteStudentAPI.as_view(), name="delete-student"),
]