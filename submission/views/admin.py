from utils.api import APIView, JSONResponse
from rest_framework import status
from ..serializers import ProblemSubmissionSerializers1
from django.http import HttpResponse, JsonResponse
from ..models import ProblemSubmission

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