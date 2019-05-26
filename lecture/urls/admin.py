from django.conf.urls import url
from lecture.views.admin import CreateLectureAPI
from lecture.views.admin import GetMyLecturesAPI
from lecture.views.admin import DeleteCourseResource
from lecture.views.admin import DeleteProblems
urlpatterns = [
    url(r'create-lectures/?$', CreateLectureAPI.as_view(), name="create-lectures"),
    url(r'get-my-lectures/?$', GetMyLecturesAPI.as_view(), name="get-my-lectures"),
    url(r'delete-file/?$', DeleteCourseResource.as_view(), name="delete-file"),
    url(r'delete-problems/?$', DeleteProblems.as_view(), name="delete-problems"),
    url(r'download-file/?$', admin.file_download,name="download-file"),
]
