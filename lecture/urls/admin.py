from django.conf.urls import url
from lecture.views.admin import CreateLectureAPI
from lecture.views.admin import GetMyLecturesAPI
from lecture.views.admin import GetLectureByNameAPI
urlpatterns = [
    url(r'create-lectures/?$', CreateLectureAPI.as_view(), name="create-lectures"),
    url(r'get-my-lectures/?$', GetMyLecturesAPI.as_view(), name="get-my-lectures"),
    url(r'get-lecture-by-name/?$', GetLectureByNameAPI.as_view(), name="get-lecture-by-name"),
]
