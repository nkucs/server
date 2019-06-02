from django.conf.urls import url

urlpatterns = [
    url(r'course-student/?$', GetStudentCourseAPI.as_view(), name="course-student"),
]