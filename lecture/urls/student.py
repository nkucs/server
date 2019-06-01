from django.conf.urls import url
from lecture.views.student import PracticeSubmission, PracticeExample
from lecture.views.student import ShowLecture

urlpatterns = [
    url(r'practice_submission/?$', PracticeSubmission.as_view(), name="practice_submission"),
    url(r'practice_example/?$', PracticeExample.as_view(), name="practice_example"),
    url(r'showlecture/?$', ShowLecture.as_view(), name="showlecture"),
    url(r"get-all-message/?$", GetAllMessage.as_view(), name="get-all-message"),
]