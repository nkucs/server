from django.conf.urls import url
from lecture.views.admin import CreateLectureAPI
from lecture.views.admin import GetMyLecturesAPI
from lecture.views.admin import DeleteCourseResource
from lecture.views.admin import DeleteProblems
from lecture.views.admin import GetLectureAPI
from ..views import admin
urlpatterns = [
    url(r'create-lectures/?$', CreateLectureAPI.as_view(), name="create-lectures"),
    url(r'get-my-lectures/?$', GetMyLecturesAPI.as_view(), name="get-my-lectures"),
    url(r'delete-file/?$', DeleteCourseResource.as_view(), name="delete-file"),
    url(r'delete-problems/?$', DeleteProblems.as_view(), name="delete-problems"),
    url(r'download-file/?$', admin.file_download,name="download-file"),
    url(r'get-lecture-by-name/?$', GetLectureByNameAPI.as_view(), name="get-lecture-by-name"),
    url(r'edit-lecture/?$', EditLectureAPI.as_view(), name="edit-lecture"),
    url(r'delete-lecture/?$', DeleteLectureAPI.as_view(), name="delet-lecture"),
    url(r'add-file/?$', AddFileAPI.as_view(), name="add-file"),
    url(r'get-lecture/?$',GetLectureAPI.as_view(), name="get-lecture")
]
