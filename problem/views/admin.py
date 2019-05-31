from ..models import Problem
from ..serializers import GetProblemSerializer,ProblemSubmissionTimeSerializers,ProblemSubmission,ProblemSubmissionCase,GetCasesSerializer,GetTagsSerializer
from ..models import Problem,Case,Tag
from utils.api import APIView, JSONResponse
from rest_framework import status
from django.http import HttpResponse, JsonResponse
class GetProblemAPI(APIView):
    """get one problem  
        by problem_id
    """
    def get(self, request):
        problem_id = int(request.GET.get('problem_id'))
        cases = []
        # query from database
        try:
            problem = Problem.objects.get(id=problem_id)
            cases_number = Case.objects.filter(problem=problem_id).count()
            cases_list = Case.objects.filter(problem=problem_id)
            for i in range(cases_number):
                case = cases_list[i]
                cases_serializer= GetCasesSerializer(case).data
                cases.append(cases_serializer)
            problem.cases = cases
        except Problem.DoesNotExist:
            return HttpResponse(status=404)
        serializer = GetProblemSerializer(problem)
        return JsonResponse(serializer.data,status=status.HTTP_200_OK)
    
class GetSubmissionsAPI(APIView):
    def get(self, request):
        list_count = 10
        # initialize the response object
        response_object = dict()
        problemSubmission = []
        page = int(request.GET.get('page'))
        problem_id = int(request.GET.get('problem_id'))
        # query from database
        try:
            problemSubmission_number = ProblemSubmission.objects.filter(problem_id=problem_id).count()
            problemSubmission_list = ProblemSubmission.objects.filter(problem_id=problem_id)
            for i in range(problemSubmission_number):
                problemSubmission_one = problemSubmission_list[i]
                problemSubmission_one.student_number = problemSubmission_one.student.student_number
                problemSubmission_one.all_cases_count = problemSubmission_one.cases.count()
                problemSubmissionCase_number =ProblemSubmissionCase.objects.filter(problem_submission=problemSubmission_one.id).count()
                problemSubmissionCase =ProblemSubmissionCase.objects.filter(problem_submission=problemSubmission_one.id)
                problemSubmission_one.succeed_cases_count = 0
                for j in range(problemSubmissionCase_number):
                    problemSubmissionCase_one = problemSubmissionCase[j]
                    if problemSubmissionCase_one.case_status.name in ['AC','ac']:
                        problemSubmission_one.succeed_cases_count += 1
                serializer = ProblemSubmissionTimeSerializers(problemSubmission_one).data
                problemSubmission.append(serializer) 
            # update response object
        except ProblemSubmission.DoesNotExist:
            return HttpResponse(status=404)
        response_object['total_pages'] = problemSubmission_number // list_count + 1
        response_object['current_page'] = page
        response_object['submissions'] = problemSubmission
        return JsonResponse(response_object,status=status.HTTP_200_OK)
