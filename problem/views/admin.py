from ..models import Problem
from ..serializers import GetProblemSerializer
from ..models import Problem
from utils.api import APIView, JSONResponse
from rest_framework import status
from django.http import HttpResponse, JsonResponse
class GetProblemAPI(APIView):
    """get one problem
        by problem_id
    """
    def get(self, request):
        problem_id = int(request.GET.get('problem_id'))
        # query from database
        try:
            problem = Problem.objects.get(id=problem_id)
        except Problem.DoesNotExist:
            return HttpResponse(status=404)
        serializer = GetProblemSerializer(problem)
        return JsonResponse(serializer.data,status=status.HTTP_200_OK)
    
