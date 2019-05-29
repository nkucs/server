from utils.api import APIView
from rest_framework import status
from ..serializers import ProblemSubmissionSerializers1
from django.http import HttpResponse, JsonResponse
from ..models import ProblemSubmission

class GetALLSubmissionAPI(APIView):
    def get(self, request):
        submission_student_id = int(request.GET.get('submission_student_id'))
        # query from database for submissions of student
        try:
            UserPersonalSubmission = ProblemSubmission.objects.get(id_student=submission_student_id)
        except UserPersonalSubmission.DoesNotExist:
            return HttpResponse(status=404)
        serializer = ProblemSubmissionSerializers1(UserPersonalSubmission)
        return JsonResponse(serializer.data,status=status.HTTP_200_OK)

class GetUserSubmissionAPI(APIView):
    def get(self, request):
        submission_student_id = int(request.GET.get('submission_student_id'))
        submission_problem_id = int(request.GET.get('submission_problem_id'))
        # query from database for submissions of student and problem 
        try:
            UserPersonalSubmission = ProblemSubmission.objects.filter(id_student=submission_student_id, id_problem=submission_problem_id)
        except ProblemSubmission.DoesNotExist:
            return HttpResponse(status=404)
        serializer = ProblemSubmissionSerializers1(ProblemSubmission)
        return JsonResponse(serializer.data,status=status.HTTP_200_OK)