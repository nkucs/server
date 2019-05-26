from utils.api import APIView
from utils.api import APIView, JSONResponse
from django.http import HttpResponse, JsonResponse
from django.db import models
from exam.models import StudentExam
from exam.models import Exam
from course.models import Course
from user.models import Student
from user.models import User

class GetExamStudentAPI(APIView):
    response_class = JSONResponse
    def post(self, request):
        exam_id = request.GET.get('exam_id')
        if not exam_id:
            #not found
            return self.error(msg=f"exam_id key is None", err=request.GET)
        try:
            # query for the lecture
            exam = Exam.objects.get(id = exam_id)
            students =exam.students
            stu_list = []
            for student in students:
                stu = StudentExam.objects.get(exam = exam,student = student)
                stu_list.append(
                    {
                        'student_number':stu.student_number,
                        'name':stu.user.name,
                        'type':stu.type,
                        'grade':stu.grade,
                        'password':stu.password,
                    }
                )
            return self.success(stu_list)
        except Exception as e:
            # not found
            return self.error(msg=str(e), err=e.args) 

class GetIdStudentAPI(APIView):
    response_class = JSONResponse
    def post(self, request):
        student_id = request.GET.get('id')
        exam_id = request.GET.get('exam_id')
        if not student_id:
                #not found
                return self.error(msg=f"student_id key is None", err=request.GET)
        try:
            # query for the lecture
            student = Student.objects.get(id = student_id)
            exam = Exam.objects.get(id = exam_id)
            stu = StudentExam.objects.get(exam = exam,student = student)
            return self.success(
                {
                    'student_number':stu.student_number,
                    'name':stu.user.name,
                    'type':stu.type,
                    'grade':stu.grade,
                    'password':stu.password,
                }
            )
        except Exception as e:
            # not found
            return self.error(msg=str(e), err=e.args)    