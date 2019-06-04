from utils.api import APIView
from utils.api import APIView, JSONResponse
from django.http import HttpResponse, JsonResponse
from django.db import models
from exam.models import StudentExam
from exam.models import Exam
from course.models import Course
from user.models import Student
from user.models import Teacher, User
from course.models import CourseTeacher, Course
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import datetime
from course.views.admin import get_course_info

class AddExamAPI(APIView):
    def post(self, request):
        try:
            courseid = request.data.get('courseid')
            name = request.data.get('name')
            start_time = request.data.get('startTime')
            end_time = request.data.get('endTime')
            description = request.data.get('description')
            exam = Exam.objects.create(
                name = name,
                start_time = start_time,
                duration = start_time-
                end_time,
                description = description,
                course_id = courseid, 
            )
            exam.save()
            return self.success(0)
        except Exception as exception:
            return self.error(err=exception.args, msg=str(exception))


class FixExamAPI(APIView):
    def post(self, request):
        try:
            examid = request.data.get('exam_id')
            name = request.data.get('name')
            start_time = request.data.get('startTime')
            end_time = request.data.get('endTime')
            description = request.data.get('description')
            exam = Exam.objects.get(id=examid)
            exam.name = name,
            exam.start_time = start_time,
            exam.duration = start_time-end_time,
            exam.description = description,
            exam.save()
            return self.success(0)
        except Exception as exception:
            return self.error(err=exception.args, msg=str(exception))

class DeleteExamAPI(APIView):
    def post(self, request):
        try:
            examid = request.data.get('exam_id')
            exam = Exam.objects.get(id = examid)
            exam.delete()
            return self.success(0)
        except Exception as exception:
            return self.error(err=exception.args, msg=str(exception))

class GetNowCourseExamAPI(APIView):
    response_class = JSONResponse
    def get(self, request):
        teacher_number = request.GET.get('teacherId')
        try:
            teacher = Teacher.objects.get(teacher_number=teacher_number)
            course_teacher = CourseTeacher.objects.filter(teacher=teacher, course__start_time__lt=datetime.date.today(), course__end_time__gt=datetime.date.today())
            course_list = []
            for course in course_teacher:
                exams = Exam.objects.filter(course = course)
                examlist =[]
                for exam in exams:
                    examlist.append({
                        'exam_id':exam.id,
                        'name':exam.name,
                        'start_time':exam.start_time,
                        'duration':exam.duration,
                        'description':exam.description,
                    })
                course_info = get_course_info(course.course)
                course_list.append({
                    'course_id':course_info['course_id'],
                    'name':course_info['name'],
                    'start_time':course_info['start_time'],
                    'end_time':course_info['end_time'],
                    'description':course_info['description'],
                    'exams':examlist,
                })
            return self.success({
                'course_list':course_list
            })
        except Exception as e:
            return self.error(msg=str(e), err=e.args)


class GetLastCourseExamAPI(APIView):
    response_class = JSONResponse
    def get(self, request):
        teacher_number = request.GET.get('teacherId')
        page_index = request.GET.get('page_index')
        page_length = request.GET.get('page_length')
        try:
            teacher = Teacher.objects.get(teacher_number=teacher_number)
            course_teacher = CourseTeacher.objects.filter(teacher=teacher, course__start_time__lt=datetime.date.today(), course__end_time__lt=datetime.date.today())
            p = Paginator(course_teacher, page_length)
            page = p.page(page_index)
            course_list = []
            for course in page:
                exams = Exam.objects.filter(course = course)
                examlist =[]
                for exam in exams:
                    examlist.append({
                        'exam_id':exam.id,
                        'name':exam.name,
                        'start_time':exam.start_time,
                        'duration':exam.duration,
                        'description':exam.description,
                    })
                course_info = get_course_info(course.course)
                course_list.append({
                    'course_id':course_info['course_id'],
                    'name':course_info['name'],
                    'start_time':course_info['start_time'],
                    'end_time':course_info['end_time'],
                    'description':course_info['description'],
                    'exams':examlist,
                })
            return self.success({
                'course_list':course_list,
                'totalPages': p.num_pages,
                'current': page_index,
            })
        except Exception as e:
            return self.error(msg=str(e), err=e.args)
    

