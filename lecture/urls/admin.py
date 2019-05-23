from django.conf.urls import url
from lecture.views.admin import CreateLectureAPI
urlpatterns = [
    url(r'create-lectures/?$', CreateLectureAPI.as_view(), name="create-lectures"),
]
