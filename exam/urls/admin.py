from django.conf.urls import url

from exam.views.admin import GetExamStudentAPI

urlpatterns = [
    url(r"get-examstudent/?$", GetExamStudentAPI.as_view(), name="get-examstudent"),
   
]