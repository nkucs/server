from django.conf.urls import url
from lecture.views.student import LectureProblemAPI, ShowLecture, ShowLectureName, GetAllMessage, DownloadSourseById

urlpatterns = [
    url(r'lecture_problem', LectureProblemAPI.as_view(), name="lecture_problem"),
    url(r'showlecture/?$', ShowLecture.as_view(), name="showlecture"),
    url(r'showlecturename/?$', ShowLectureName.as_view(), name="showlecturename"),
    url(r"get-all-message/?$", GetAllMessage.as_view(), name="get-all-message"),
    url(r"download-sourse/?$", DownloadSourseById.as_view(), name="download-sourse"),
]