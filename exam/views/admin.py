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
                'password': 'xxxxxxxxxxxxxxxxxxxx',
                'type': i.type
            })
        return self.success({
			'totalPages':p.num_pages,
			'current':page_index,
			'students': results
			})


class GetIdStudentAPI(APIView):
    def get(self, request):
        student_id = request.GET.get('id')
        exam_id = request.GET.get('exam')
        if not student_id:
            return self.error(msg=f"student_id key is None", err=request.GET)
        try:
            # query for the lecture
            student = Student.objects.get(id = student_id)
            exam = Exam.objects.get(id = exam_id)
            stu = StudentExam.objects.get(exam = exam,student = student)
            stu_list = []
            stu_list.append(
                    {
                        'student_number':stu.student.student_number,
                        'name':stu.student.user.name,
                        'type':stu.type,
                        'grade':stu.grade,
                        'password':stu.password,
                    }
                )
            return self.success(stu_list)
        except Exception as e:
            # not found
            return self.error(msg=str(e), err=e.args)    

class GetNameStudentAPI(APIView):
    def get(self, request):
        student_name = request.GET.get('name')
        exam_id = request.GET.get('exam_id')
        if not student_name:
                #not found
                return self.error(msg=f"student_name key is None", err=request.GET)
        try:
            # query for the lecture
            students = User.objects.fliter(name = student_name)
            exam = Exam.objects.get(id = exam_id)
            stu_list = []
            for student in students:
                stu = StudentExam.objects.get(exam = exam,student = student)
                stu_list.append(
                    {
                        'student_number':stu.student.student_number,
                        'name':stu.student.user.name,
                        'type':stu.type,
                        'grade':stu.grade,
                        'password':stu.password,
                    }
                )
            return self.success(stu_list)
        except Exception as e:
            # not found
            return self.error(msg=str(e), err=e.args)    
 
class GetIdStuAllAPI(APIView):
    def get(self, request):
        student_id = request.GET.get('id')
        stu_list = []
        if not student_id:
                #not found
                return self.error(msg=f"student_id key is None", err=request.GET)
        try:
            # query for the lecture
            student = Student.objects.get(id = student_id)
            stu_list.append(
                    {
                        'student_number':student.student_number,
                        'name':student.user.name,
                        'room':student.room,
                    }
                )
            return self.success(stu_list)
        except Exception as e:
            # not found
            return self.error(msg=str(e), err=e.args)    

class GetNameStuAllAPI(APIView):
    def get(self, request):
        student_name = request.data.get('name')
        if not student_name:
                #not found
                return self.error(msg=f"student_name key is None", err=request.GET)
        try:
            # query for the lecture
            students = User.objects.fliter(name = student_name)
            stu_list = []
            for student in students:
                stu_list.append(
                    {
                        'student_number':student.student_number,
                        'name':student.user.name,
                        'room':student.room,
                    }
                )
            return self.success(stu_list)
        except Exception as e:
            # not found
            return self.error(msg=str(e), err=e.args)    

class AddStudentAPI(APIView):
    def post(self, request):
        exam_id = request.data.get('exam')
        id = request.data.get('id')
        num = len(id)
        stu_list = []
        # exam = Exam.objects.get(id = exam_id)
        for i in range(num):
            stu_list.append(i)
            # stu = Student.objects.get(id = id[i])
            # student = StudentExam.objects.create(
            #     student = stu,
            #     exam = exam,
            #     type = 'A', 
            #     grade = '',
            #     password = 1,
            #     finished = '',
            #     problem_submissions = '', 
            # )
            # student.save()
        # students =exam.students
        # for student in students:
        #     stu = StudentExam.objects.get(exam = exam,student = student)
        #     stu_list.append(
        #         {
        #                 'student_number':stu.student_number,
        #                 'name':stu.user.name,
        #                 'type':stu.type,
        #                 'grade':stu.grade,
        #                 'password':stu.password,
        #         }
        #     )
        return self.success(stu_list)
        
class DeleteStudentAPI(APIView):
    def post(self, request):
        exam_id = request.data.get('exam')
        id = request.data.get('id')
        num = len(id)
        exam = Exam.objects.get(id = exam_id)
        for i in range(num):
            stu = Student.objects.get(id = id[i])
            student = StudentExam.objects.get(exam = exam,student = stu)
            student.delete()
        return self.success(0)

class FixStudentAPI(APIView):
    def post(self, request):
        exam_id = request.data.get('exam')
        id = request.data.get('id')
        typed = request.data.get('type')
        exam_id = request.data.get('exam_id')
        password = request.data.get('password')

        if not exam_id:
            #not found
            return self.error(msg=f"exam_id key is None", err=request.GET)
        try:
            exam = Exam.objects.get(id = exam_id)
            stu = Student.objects.get(id = id[i])
            student = StudentExam.objects.get(exam = exam,student = stu)
            student.type = typed
            student.grade = exam_id
            student.password = password
            student.save()
            return self.success(0)
            # query for the lecture
            
        except Exception as e:
            # not found
            return self.error(msg=str(e), err=e.args)

class GetAllStudentAPI(APIView):
    def post(self, request):
        students = Student.objects.all()
        if not students:
            #not found
            return self.error(msg=f"exam_id key is None", err=request.GET)
        try:
            return self.success(students)
            # query for the lecture      
        except Exception as e:
            # not found
            return self.error(msg=str(e), err=e.args)
     

        
      
