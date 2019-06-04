"""oj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title="NKCS-OPEP API")


urlpatterns = [
    url(r"^api/", include("demo.urls.oj")),
    url(r"^teacher/lab/", include("lab.urls.admin")),
    url(r"^teacher/submission/", include("submission.urls.admin")),
    url(r"^teacher/lecture/", include("lecture.urls.admin")),
    url(r"^administrator/role/", include("user.urls.admin")),
    url(r"^administrator/staff/", include("user.urls.admin_staff")),
    url(r"^exam/student", include("exam.urls.admin")),
    url(r"^exam/examlist", include("exam.urls.admin")),
    url(r"^teacher/course/", include("course.urls.admin")),
    url(r"^api/student/lab/", include("lab.urls.student")),
    url(r"^api/student/course/", include("course.urls.student")),
    url(r"^teacher/course/stat/", include("course.urls.statistics")),
    url(r"^teacher/submission/stat/", include("submission.urls.statistics")),
    url(r"^teacher/student/stat/", include("user.urls.statistics")),
    url(r"^api/student/submission", include("submission.urls.student")),
    url(r"^api/student/problem", include("problem.urls.student")),
    url(r"^api/student/user", include("user.urls.student")),
    url(r"^statistic/course/", include("course.urls.statistics")),
    url(r"^api/student/", include("lab.urls.student")),
    url(r"^student/lab/", include("lab.urls.student")),
    url(r"^auth/", include("user.urls.auth")),
    url(r"^swagger$", schema_view),
    url(r"^teacher/problem/", include("problem.urls.admin")),
    url(r"^teacher/submission/statistics/",include("submission.urls.statistics")),
    url(r"^distribution/", include("submission.urls.statistics")),
]
