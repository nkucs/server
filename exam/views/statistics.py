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
from problem.models import Problem
from exam.models import ExamProblem
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import datetime

class GetAllProblemAPI(APIView):
    response_class = JSONResponse
    def get(self, request):
        page_index = request.GET.get('page_index')
        page_length = request.GET.get('page_length')
        search_name = request.GET.get('search_name')
        search_number = request.GET.get('search_number')
        try:
            problems = Problem.objects.filter(name__icontains=search_name, code__icontains=search_number)
            problem_list = []
            for problem in problems:
                problem_list.append({
                    "id": problem.id,
                    "key": problem.id,
                    "code": problem.code,
                    "name": problem.name
                })            
            p = Paginator(problem_list, page_length)
            page = p.page(page_index)
            results = []
            for i in page:
                results.append(i)
            return self.success({
                'problem_list':results,
                'totalPages': p.num_pages,
                'current': page_index,
            })
        except Exception as e:
            return self.error(msg=str(e), err=e.args)

class AddExamAPI(APIView):
    def post(self, request):
        #try:
        courseid = request.data.get('courseid')
        name = request.data.get('name')
        start_time = request.data.get('startTime')[:19]
        end_time = request.data.get('endTime')[:19]
        description = request.data.get('description')
        examPage = request.data.get('examPage')
        language = int(request.data.get('language'))
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S")
        exam = Exam.objects.create(
            name = name,
            start_time = start_time,
            duration = end_time - start_time,
            description = description,
            course_id = courseid, 
        )
        exam.save()
        language = 1 << language
        for i in range(1, len(examPage)):
            for pro in examPage[i]:
                problem = Problem.objects.get(id = pro['id'])
                examproblem = ExamProblem.objects.create(
                    problem = problem,
                    exam_id = exam.id,
                    weight = 1,
                    language = language,
                    type = i,
                )
                examproblem.save()

        return self.success(0)
        #except Exception as exception:
            #return self.error(err=exception.args, msg=str(exception))


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

def toTimeString(mydatetime):
    year = str(mydatetime.year) + " 年"
    month = str(mydatetime.month) + " 月"
    day = str(mydatetime.day) + " 日"
    hour = str(mydatetime.hour) + " 时"
    minute = str(mydatetime.minute) + " 分"
    second = str(mydatetime.second) + " 秒"
    return year + " " + month + " " + day + " " + hour + " " + minute + " " + second

def toDurationString(myduration):
    second = int(myduration.seconds) % 60
    minute = int(myduration.seconds) % 3600 // 60
    hour = int(myduration.seconds) // 3600
    day = myduration.days

    day = str(day) + "天" if day > 0 else ""
    hour = str(hour) + "小时" if hour > 0 else ""
    minute = str(minute) + "分钟" if minute > 0 else ""
    second = str(second) + "秒"
    return day + " " + hour + " " + minute + " " + second

class GetNowCourseExamAPI(APIView):
    response_class = JSONResponse
    def get(self, request):
        teacher_id = request.GET.get('teacher_id')
        page_index = request.GET.get('page_index')
        page_length = request.GET.get('page_length')
        try:
            course_teachers = CourseTeacher.objects.filter(teacher__id=teacher_id, course__start_time__lt=datetime.date.today(), course__end_time__gt=datetime.date.today())
            course_list = []
            for course_teacher in course_teachers:
                exams = Exam.objects.filter(course = course_teacher.course)
                examlist = []
                for exam in exams:
                    examlist.append({
                        'exam_id':exam.id,
                        'key': str(exam.id),
                        'title':exam.name,
                        'starttime':toTimeString(exam.start_time),
                        'duration':toDurationString(exam.duration),
                        'content':exam.description,
                    })
                course_info = course_teacher.course
                course_list.append({
                    'id':course_info.id,
                    'code':course_info.code,
                    'name':course_info.name,
                    'starttime':course_info.start_time,
                    'endtime':course_info.end_time,
                    'description':course_info.description,
                    'exampanes':examlist,
                    'activeKey': '1',
                })
            p = Paginator(course_list, page_length)
            page = p.page(page_index)
            results = []
            for i in page:
                results.append(i)
            return self.success({
                'course_list':results,
                'totalPages': p.num_pages,
                'current': page_index,
            })
        except Exception as e:
            return self.error(msg=str(e), err=e.args)


class GetLastCourseExamAPI(APIView):
    response_class = JSONResponse
    def get(self, request):
        teacher_id = request.GET.get('teacher_id')
        page_index = request.GET.get('page_index')
        page_length = request.GET.get('page_length')
        try:
            course_teachers = CourseTeacher.objects.filter(teacher__id=teacher_id, course__start_time__lt=datetime.date.today(), course__end_time__lt=datetime.date.today())
            course_list = []
            for course_teacher in course_teachers:
                exams = Exam.objects.filter(course = course_teacher.course)
                examlist = []
                for exam in exams:
                    examlist.append({
                        'exam_id':exam.id,
                        'key': str(exam.id),
                        'title':exam.name,
                        'starttime':exam.start_time,
                        'duration':exam.duration,
                        'content':exam.description,
                    })
                course_info = course_teacher.course
                course_list.append({
                    'id':course_info.id,
                    'code':course_info.code,
                    'name':course_info.name,
                    'starttime':course_info.start_time,
                    'endtime':course_info.end_time,
                    'description':course_info.description,
                    'exampanes':examlist,
                    'activeKey': '1',
                })
            p = Paginator(course_list, page_length)
            page = p.page(page_index)
            results = []
            for i in page:
                results.append(i)
            return self.success({
                'course_list':results,
                'totalPages': p.num_pages,
                'current': page_index,
            })
        except Exception as e:
            return self.error(msg=str(e), err=e.args)
    

