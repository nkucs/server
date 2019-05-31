from utils.api import APIView, JSONResponse
from rest_framework import status
from ..serializers import ProblemSubmissionSerializers1
from django.http import HttpResponse, JsonResponse
from ..models import Role, Permission, Student

def GetStudentAPI(APIView):
    def get(self, request):
        # get information from frontend
        id_student = int(request.GET.get('id_student'))
        try:
            NowStudent = Student.objects.get(id=id_student) 
        except NowStudent.DoesNotExist:
            return HttpResponse(status=404)
        serializer = ProblemSubmissionSerializers1(NowStudent)
        return JsonResponse(serializer.data,status=status.HTTP_200_OK)

def LoginStudentAPI(APIView):
    # Login API
    def post(self, request):
        studentName = request.GET.get('name')
        studentPasswordHash = request.GET.get('password_hash')
        studentUser = Student.objects.get(name=studentName)
        if studentUser:
            if studentUser.password_hash == studentPasswordHash:
                return HttpResponse(status=0)
            else:
                return HttpResponse(status=1)
        else:
            return HttpResponse(status=-1)