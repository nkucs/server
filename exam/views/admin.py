from utils.api import APIView
from utils.api import APIView, JSONResponse
from django.http import HttpResponse, JsonResponse
from django.db import models
from exam.models import StudentExam
from exam.models import Exam
from course.models import Course
from user.models import Student
from user.models import User
from django.core.paginator import Paginator
import random

def hash(key):
    key += ~(key << 15)
    key ^= (key >> 10)
    key += (key << 3)
    key ^= (key >> 6)
    key += ~(key << 11)
    key ^= (key >> 16)
    return key

class GetExamStudentAPI(APIView):
    def get(self, request):
        exam_id = request.GET.get('exam_id')
        student_name = request.GET.get('student_name')
        student_number = request.GET.get('student_number')
        page_index = request.GET.get('page_index')
        page_length = request.GET.get('page_length')
        studentexams = StudentExam.objects.filter(exam_id=exam_id, student__student_number__icontains=student_number,
                                                  student__user__name__icontains=student_name)
        p = Paginator(studentexams, page_length)
        page = p.page(page_index)
        results = []
        for i in page:
            results.append({
                'number': i.student.student_number,
                'name': i.student.user.name,
                'password': i.password,
                'type': i.type
            })
        return self.success({
            'totalPages': p.num_pages,
            'current': page_index,
            'students': results
        })


class GetAllStudentAPI(APIView):
    def get(self, request):
        
        exam_id = request.GET.get('exam_id')
        student_name = request.GET.get('student_name')
        student_number = request.GET.get('student_number')
        page_index = request.GET.get('page_index')
        page_length = request.GET.get('page_length')
        examstudents = StudentExam.objects.filter(exam__id=exam_id)
        examid = []
        for stu in examstudents:
            examid.append(stu.student.student_number)
            
        student = Student.objects.exclude(student_number__in=examid).filter(student_number__icontains=student_number,
                                                                                   user__name__icontains=student_name)
       

        p = Paginator(student, page_length)
        page = p.page(page_index)
        results = []
        for i in page:
            results.append({
                'all_id': i.student_number,
                'all_name': i.user.name,
                'all_class': i.room,
            })
        return self.success({
            'totalPages': p.num_pages,
            'current': page_index,
            'students': results
        })

def getrandompassword(number):
    x = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    result = ""
    for i in range(number):
        result += x[random.randint(0, len(x) - 1)]
    return result

class AddStudentAPI(APIView):
    def post(self, request):
        exam_id = request.data.get('exam_id')
        number = request.data.get('number')
        num = len(number)
        exam = Exam.objects.get(id=exam_id)
        try:
            for i in range(num):
                stu = Student.objects.get(student_number=number[i])
                student = StudentExam.objects.create(
                    student=stu,
                    exam=exam,
                    type=0,
                    grade=0,
                    password=getrandompassword(10),
                    finished=0,
                )
                student.save()
            return self.success(0)
        except Exception as e:

            return self.error(msg=str(e), err=e.args)


class DeleteStudentAPI(APIView):
    def post(self, request):
        exam_id = request.data.get('exam')
        stunums = request.data.get('stunums')
        num = len(stunums)
        exam = Exam.objects.get(id=exam_id)
        try:
            for i in range(num):
                student = StudentExam.objects.get(exam=exam, student__student_number=stunums[i])
                student.delete()
            return self.success(0)
        except Exception as e:

            return self.error(msg=str(e), err=e.args)



class FixStudentAPI(APIView):
    def post(self, request):
        exam_id = request.data.get('exam_id')
        student_number = request.data.get('student_number')
        typed = request.data.get('type')
        password = request.data.get('password')
        try:
            exam = Exam.objects.get(id=exam_id)
            student = StudentExam.objects.get(exam=exam, student__student_number=student_number)
            student.type = typed
            student.password = password
            student.save()
            return self.success(0)
        except Exception as e:
            # not found
            return self.error(msg=str(e), err=e.args)


class GetAllContentAPI(APIView):
    def post(self, request):
        exam_id = request.data.get('exam_id')
        student_number = request.data.get('student_number')
        exam = Exam.objects.get(id=exam_id)
        stu_list = []
        try:
            student = StudentExam.objects.filter(exam=exam, student__student_number__in=student_number)
            for i in student:
                stu_list.append({
                    'number': i.student.student_number,
                    'name': i.student.user.name,
                    'password': i.password,
                    'type': i.type
                })

            return self.success({'stu_list': stu_list})
        except Exception as e:
            # not found
            return self.error(msg=str(e), err=e.args)
