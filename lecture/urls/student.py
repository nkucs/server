from django.conf.urls import url
from lecture.views.student import LectureProblem
from lecture.views.student import ShowLecture, ShowLectureName
from lecture.views.student import GetAllMessage, DownloadSourseById

urlpatterns = [
    url(r'showlecture/?$', ShowLecture.as_view(), name="showlecture"),
    url(r'showlecturename/?$', ShowLectureName.as_view(), name="showlecturename"),
    url(r"get-all-message/?$", GetAllMessage.as_view(), name="get-all-message"),
    url(r"download-sourse/?$", DownloadSourseById.as_view(), name="download-sourse"),
    url(r'lecture_problem', LectureProblem.as_view(), name="lecture_problem"),
]