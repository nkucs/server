from utils.api import APIView, JSONResponse
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from ..models import Problem, Case
from django.forms import model_to_dict

class GetProblemAPI(APIView):
    def get(self, request):
        # get information from frontend #ok#
        id_problem = int(request.GET.get('id_problem'))
        problem_return = model_to_dict(Problem.objects.get(id=id_problem))
        del problem_return['tags']
        return self.success(problem_return)


class GetCaseOfProblemAPI(APIView):
    def get(self, request):
        # get information from frontend #ok#
        id_problem = int(request.GET.get('id_problem'))
        case_list = Case.objects.filter(problem=id_problem)
        case_list_result = []
        for item in case_list:
            item_result = model_to_dict(item)
            del item_result['tags']
            case_list_result.append(item_result)
        return self.success(case_list_result)
