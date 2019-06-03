from django.conf.urls import url
from course.views.statistics import GetTeacherCoursesAPI
from course.views.statistics import GetProblemDataAPI
from course.views.statistics import GetCourseStudentNumberAPI


urlpatterns = [
    url(r"^problem-data/?$", GetProblemDataAPI.as_view(), name="problem-data"),
    url(r"^get-teacher-courses/?$", GetTeacherCoursesAPI.as_view(), name="get-teacher-courses"),
    url(r"^get-course-student-number/?$",
        GetCourseStudentNumberAPI.as_view(), name="get-course-student-number"),
]