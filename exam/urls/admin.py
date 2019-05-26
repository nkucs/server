from django.conf.urls import url

from exam.views.admin import GetExamStudentAPI
from exam.views.admin import GetIdStudentAPI
from exam.views.admin import GetNameStudentAPI

urlpatterns = [
    url(r"get-examstudent/?$", GetExamStudentAPI.as_view(), name="get-examstudent"),
    url(r"get-idstudent/?$", GetIdStudentAPI.as_view(), name="get-idstudent"),
    url(r"get-namestudent/?$", GetNameStudentAPI.as_view(), name="get-namestudent"),
]