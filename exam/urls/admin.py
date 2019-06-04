from django.conf.urls import url

from exam.views.admin import GetExamStudentAPI
from exam.views.admin import AddStudentAPI
from exam.views.admin import DeleteStudentAPI
from exam.views.admin import FixStudentAPI
from exam.views.admin import GetAllStudentAPI
from exam.views.admin import GetAllContentAPI
from exam.views.statistics import AddExamAPI
from exam.views.statistics import DeleteExamAPI
from exam.views.statistics import FixExamAPI
from exam.views.statistics import GetNowCourseExamAPI
from exam.views.statistics import GetLastCourseExamAPI
from exam.views.statistics import GetAllProblemAPI

urlpatterns = [
    url(r"get-allcontent/?$", GetAllContentAPI.as_view(), name="get-allcontent"),
    url(r"add-student/?$", AddStudentAPI.as_view(), name="add-student"),
    url(r"delete-student/?$", DeleteStudentAPI.as_view(), name="delete-student"),
    url(r"fix-student/?$", FixStudentAPI.as_view(), name="fix-student"),
    url(r"get-allstudent/?$", GetAllStudentAPI.as_view(), name="get-allstudent"),
    url(r"get-examstudent/?$", GetExamStudentAPI.as_view(), name="get-examstudent"),
    url(r"add-exam/?$",AddExamAPI.as_view(), name="add-exam"),
    url(r"delete-exam/?$",DeleteExamAPI.as_view(), name="delete-exam"),
    url(r"fix-exam/?$",FixExamAPI.as_view(), name="fix-exam"),
    url(r"get-nowexam/?$",GetNowCourseExamAPI.as_view(), name="get-nowexam"),
    url(r"get-lastexam/?$",GetLastCourseExamAPI.as_view(), name="get-lastexam"),
    url(r"get-allproblem/?$", GetAllProblemAPI.as_view(), name="get-allproblem"),
]