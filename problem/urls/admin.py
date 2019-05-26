from django.urls import path
from ..views.admin import GetProblemsAPI

urlpatterns = [
    path('get-all-problems/', GetProblemsAPI.as_view(), name='get-all-problems'),
]
