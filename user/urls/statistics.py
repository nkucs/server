from django.conf.urls import url
from ..views.statistics import GetStudentStatAPI

urlpatterns = [
    url(r"^get_student_num_by_year/?$", GetStudentStatAPI.as_view(), name="get_student_num_by_year"),
]
