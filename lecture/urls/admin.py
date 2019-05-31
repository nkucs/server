from django.conf.urls import url
from lecture.views.admin import CreateLectureAPI
from lecture.views.admin import GetMyLecturesAPI
from lecture.views.admin import GetLectureByNameAPI
from lecture.views.admin import EditLectureAPI
from lecture.views.admin import DeleteLectureAPI
from lecture.views.admin import AddFileAPI
urlpatterns = [
    url(r'create-lectures/?$', CreateLectureAPI.as_view(), name="create-lectures"),
    url(r'get-my-lectures/?$', GetMyLecturesAPI.as_view(), name="get-my-lectures"),
    url(r'get-lecture-by-name/?$', GetLectureByNameAPI.as_view(), name="get-lecture-by-name"),
    url(r'edit-lecture/?$', EditLectureAPI.as_view(), name="edit-lecture"),
    url(r'delete-lecture/?$', DeleteLectureAPI.as_view(), name="delet-lecture"),
    url(r'add-file/?$', AddFileAPI.as_view(), name="add-file"),
]
