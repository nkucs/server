from ..models import Problem
from ..serializers import GetProblemSerializer, GetProblemsSerializer
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

class GetProblemsAPI(APIView):
    response_class = JSONResponse
    def get(self, request):
        response_object = dict()
        try:
            current_page = int(request.GET.get('page'))
        except Exception as exception:
            return self.error(err=exception.args, msg="No page")
        
        try:
            # query from database
            problem_list = Problem.objects.all()
            
            # update response object
            response_object['total_pages'] = 10
            response_object['current_page'] = current_page
            response_object['problems'] = GetProblemsSerializer(problem_list, many=True).data

            return self.success(response_object)
        except Exception as exception:
            return self.error(err=exception.args, msg=str(exception))
    
