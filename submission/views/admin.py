from utils.api import APIView, JSONResponse
from rest_framework import status
from ..serializers import ProblemSubmissionSerializers1,ProblemSubmissionTimeSerializers
from django.http import HttpResponse, JsonResponse
from ..models import ProblemSubmission,Student,ProblemSubmissionCase
import datetime
from rest_framework.renderers import JSONRenderer
class GetSubmissionAPI(APIView):
    def get(self, request):
        
        submission_id = int(request.GET.get('submission_id'))
        # query from database
        try:
            problemSubmission = ProblemSubmission.objects.get(id=submission_id)
        except ProblemSubmission.DoesNotExist:
            return HttpResponse(status=404)
        serializer = ProblemSubmissionSerializers1(problemSubmission)
        
        return JsonResponse(serializer.data,status=status.HTTP_200_OK)


class GetSubmissionsAPI(APIView):
    def post(self, request):
        list_count = 10
        # initialize the response object
        response_object = dict()
        problemSubmission = []
        page = int(request.POST.get('page'))
        begin_time =request.POST.get('begin_time')
        end_time =request.POST.get('end_time')
        date_from=datetime.datetime.strptime(begin_time, "%Y-%m-%d %H:%M:%S")
        date_to=datetime.datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        # query from database
        try:
            problemSubmission_number = ProblemSubmission.objects.filter(created_at__range=(date_from, date_to)).count()
            problemSubmission_list = ProblemSubmission.objects.filter(created_at__range=(date_from, date_to))
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