from django.conf.urls import url

from exam.views.admin import GetExamStudentAPI
from exam.views.admin import GetIdStudentAPI
from exam.views.admin import GetNameStudentAPI
from exam.views.admin import AddStudentAPI
from exam.views.admin import DeleteStudentAPI
from exam.views.admin import FixStudentAPI
from exam.views.admin import GetAllStudentAPI
from exam.views.admin import GetIdStuAllAPI
from exam.views.admin import GetNameStuAllAPI

urlpatterns = [
    url(r"get-examstudent/?$", GetExamStudentAPI.as_view(), name="get-examstudent"),
    url(r"get-idstudent/?$", GetIdStudentAPI.as_view(), name="get-idstudent"),
    url(r"get-namestudent/?$", GetNameStudentAPI.as_view(), name="get-namestudent"),
    url(r"add-student/?$", AddStudentAPI.as_view(), name="add-student"),
    url(r"delete-student/?$", DeleteStudentAPI.as_view(), name="delete-student"),
    url(r"fix-student/?$", FixStudentAPI.as_view(), name="fix-student"),
    url(r"get-allstudent/?$", GetAllStudentAPI.as_view(), name="get-allstudent"),
    url(r"get-idstuall/?$", GetIdStuAllAPI.as_view(), name="get-idstuall"),
    url(r"get-namestuall/?$", GetNameStuAllAPI.as_view(), name="get-namestuall"),
]