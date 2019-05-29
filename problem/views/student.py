from utils.api import APIView, JSONResponse
from rest_framework import status
from ..serializers import ProblemSubmissionSerializers1
from django.http import HttpResponse, JsonResponse
from ..models import Problem

def GetProblemAPI():
    def get(self, request):
        # get information from frontend
        id_problem = int(request.GET.get('id_problem'))
        try:
            Problem = Problem.objects.get(id=id_problem) 
        except Problem.DoesNotExist:
            return HttpResponse(status=404)
        serializer = ProblemSubmissionSerializers1(Problem)
        return JsonResponse(serializer.data,status=status.HTTP_200_OK)