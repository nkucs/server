from django.conf.urls import url
from lecture.views.admin import CreateLectureAPI
from lecture.views.admin import GetMyLecturesAPI
urlpatterns = [
    url(r'create-lectures/?$', CreateLectureAPI.as_view(), name="create-lectures"),
    url(r'get-my-lectures/?$', GetMyLecturesAPI.as_view(), name="get-my-lectures"),
]
