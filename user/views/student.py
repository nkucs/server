from utils.api import APIView, JSONResponse
from rest_framework import status
from ..serializers import ProblemSubmissionSerializers1
from django.http import HttpResponse, JsonResponse
from ..models import Role, Permission, Student

def GetStudentAPI():
    def get(self, request):
        # get information from frontend
        id_student = int(request.GET.get('id_student'))
        try:
            Student = Student.objects.get(id=id_student) 
        except Student.DoesNotExist:
            return HttpResponse(status=404)
        serializer = ProblemSubmissionSerializers1(Student)
        return JsonResponse(serializer.data,status=status.HTTP_200_OK)
