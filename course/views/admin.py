from utils.api import APIView, JSONResponse
from django.http import HttpResponse, JsonResponse
from django.db import models
from user.models import Teacher, User
from course.models import CourseTeacher, Course
from lecture.models import *
from exam.models import *
from lab.models import *
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import datetime

def get_course_info(course):
    course_info = dict()
    course_info['course_id'] = course.code
    course_info['name'] = course.name
    course_info['start_time'] = course.start_time
    course_info['end_time'] = course.end_time
    course_info['description'] = course.description
    teachers = course.teachers.objects.all()
    teacher_name_list = list()
    for teacher in teachers:
        teacher_name_list.append(teacher.user.name)
    course_info['teachers'] = teacher_name_list
    return course_info

def select_course_by_teacher(teacher):
    course_list = set()
    teacher_courses = CourseTeacher.objects.filter(teacher__icontains=teacher)
    for teacher_course in teacher_courses:
        course_list.add(teacher_course.course)
    return course_list

def select_course_by_name(name):
    course_list = set()
    courses = Course.objects.filter(name__icontains=name)
    for course in courses:
        course_list.add(course)
    return course_list

def get_course_all():
    course_list = set()
    courses = Course.objects.all()
    for course in courses:
        course_list.add(course)
    return course_list


class GetNowCourseAPI(APIView):
    response_class = JSONResponse
    def get(self, request):
        response = dict()
        teacher_number = request.GET.get('teacherId')
        try:
            teacher = Teacher.objects.get(teacher_number=teacher_number)
            courses_teacher = CourseTeacher.objects.filter(teacher=teacher, course__start_time__lt=datetime.date.today(), course__end_time__gt=datetime.date.today())
            courses_info = list()
            for course in courses_teacher:
                courses_info.push(get_course_info(courses_teacher.course))
            response['courseList'] = courses_info
            return self.success(response)
        except Exception as e:
            return self.error(msg=str(e), err=e.args)
            

class GetAllCourseAPI(APIView):
    response_class = JSONResponse
    def get(self, request):
        response = dict()
        page_length = request.GET.get('pageLength')
        page = request.GET.get('page')
        teacher = request.GET.get('teacher')
        name = request.GET.get('name')
        try:
            courses = get_course_all()
            if teacher != None:
                course_list_by_teacher = select_course_by_teacher(teacher)
                courses = courses.intersection(course_list_by_teacher)
            if name != None:
                course_list_by_name = select_course_by_name(name)
                courses = courses.intersection(course_list_by_name)
            courses = list(courses)
            paginator = Paginator(courses, page_length)
            try:
                courses = paginator.page(page)
                response['currentPage'] = page
            except PageNotAnInteger:
                courses = paginator.page(1)
                response['currentPage'] = 1
            except EmptyPage:
                courses = paginator.page(paginator.num_pages)
                response['currentPage'] = paginator.num_pages
            response['totalPages'] = paginator.num_pages
            courses_info = list()
            for course in courses:
                courses_info.push(course)
            response['courses'] = courses_info
            return self.success(response)
        except Exception as e:
            return self.error(msg=str(e), err=e.args)


class GetMyCourseAPI(APIView):
    response_class = JSONResponse
    def get(self, request):
        esponse = dict()
        teacher_number = request.GET.get('teacherNumber')
        page_length = request.GET.get('pageLength')
        page = request.GET.get('page')
        try:
            teacher = Teacher.objects.get(teacher_number=teacher_number)
            courses_teacher = CourseTeacher.objects.filter(teacher=teacher)
            paginator = Paginator(courses_teacher, page_length)
            response['totalPages'] = paginator.num_pages
            try:
                courses_teacher = paginator.page(page)
                response['currentPage'] = page
            except PageNotAnInteger:
                courses_teacher = paginator.page(1)
                response['currentPage'] = 1
            except EmptyPage:
                courses_teacher = paginator.page(paginator.num_pages)
                response['currentPage'] = paginator.num_pages
            courses = list()
            for course in courses_teacher:
                courses.append(course.course)
            courses_info = list()
            for course in courses:
                courses_info.push(course)
            response['courses'] = courses_info
            return self.success(response)
        except Exception as e:
            return self.error(msg=str(e), err=e.args)


class DeleteCourseAPI(APIView):
    response_class = JSONResponse
    def post(self, request):
        '''删除课程'''
        course_code = request.POST.get('courseCode')
        if not Course.objects.filter(code=course_code).exists():
            return self.error(msg=f"course not exist", err=request.POST)
        else:
            try:
                course = Course(code=course_code, deleted=True)
                course.save()
            except Exception as e:
                return self.error(msg=str(e), err=e.args)


class DuplicateCourseAPI(APIView):
    response_class = JSONResponse
    def post(self, request):
        course_code = request.POST.get('courseCode')
        if not Course.objects.filter(code=course_code).exists():
            return self.error(msg=f"course not exist", err=request.POST)
        else:
            try:
                # 赋予复制后的课程新code并返回该code，新课其余信息与原课一致
                codes = [int(course.code) for course in Course().objects]
                new_course_code = str(max(codes)+1)
                course = Course(code=course_code)
                Course.objects.create(code=new_course_code, name=course.name,
                                      start_time=course.start_time, end_time=course.end_time,
                                      description=course.description, deleted=course.deleted,
                                      students=course.students, teachers=course.teachers)
                return self.success(new_course_code)
            except Exception as e:
                return self.error(msg=str(e), err=e.args)


class AddCourseAPI(APIView):
    response_class = JSONResponse
    def post(self, request):
        try:
            name = request.POST.get('name')
            start_time = request.POST.get('startTime')
            end_time = request.POST.get('endTime')
            description = request.POST.get('description')
            course = Course.objects.create(
                name = name,
                start_time = start_time,
                end_time = end_time,
                description = description,
            )
            course.save()
            return self.success(0)
        except Exception as exception:
            return self.error(err=exception.args, msg=str(exception))


class UpdateAPI(APIView):
    response_class = JSONResponse
    def post(self, request):
        try:
            teacher_number = request.POST.get('teacherNumber')
            course_code = request.POST.get('courseCode')
            name = request.POST.get('name')
            start_time = request.POST.get('startTime')
            end_time = request.POST.get('endTime')
            description = request.POST.get('description')
            teacher = Teacher.objects.filter(teacher_number=teacher_number)
            course = Course.objects.filter(code=course_code).update(name=name, start_time=start_time, end_time=end_time, description=description)
            return self.success(0)
        except Exception as exception:
            return self.error(err=exception.args, msg=str(exception))

class GetCourseDetailsAPI(APIView):
    response_class = JSONResponse
    def get(self, request):
        teacher_number = request.GET.get('teacherNumber')
        if not teacher_number:
            #not found
            return self.error(msg=f"teacher_number key is None", err=request.GET)
        try:
            teacher = Teacher.objects.get(teacher_number=teacher_number)
            courses_teacher = CourseTeacher.objects.filter(teacher=teacher)
            courses = []
            cur_time = datetime.date.today()
            for course_teacher in courses_teacher:
                cur_course = course_teacher.course
                s_time = cur_course.start_time
                e_time = cur_course.end_time
                if cur_time.le(e_time) and cur_time.ge(s_time): 
                    courses.append(
                        {
                            'course_id' : cur_course.code,
                            'name' : cur_course.name,
                            'start_time' : cur_course.start_time,
                            'end_time' : cur_course.end_time,
                            'description' : cur_course.description
                        }
                    )
            return self.success(JSONResponse(courses))
        except Exception as e:
            # not found
            return self.error(msg=str(e), err=e.args)

class GetMyStudentsAPI(APIView):
    def get(self, request):
        page = request.GET.get("page")
        page_length = request.GET.get("page_length")
        student_number = request.GET.get("student_number")
        student_name = request.GET.get("student_name")
        course_id = request.GET.get("course_id")
        course = Course.objects.get(id=course_id)
        students = course.students.all().filter(student_number__icontains=student_number, user__name__icontains=student_name)
        paginator = Paginator(students, page_length)
        students = paginator.page(page)
        results = []
        for student in students:
            results.append({
                'key' : student.id,
                'name' : student.user.name,
                'number' : student.student_number,
                'description' : "没有描述"
            })
        return self.success({'students':results,
            'totalPages':paginator.num_pages,
            'current': page,
            'all_student': len(results)})
            
class GetMyProblemsAPI(APIView):
    def get(self, request):
        page = request.GET.get("page")
        page_length = request.GET.get("page_length")
        problem_name = request.GET.get("problem_name")
        course_id = request.GET.get("course_id")
        course = Course.objects.get(id=course_id)
        problems = []
        '''Now for lectures'''
        lectures = Lecture.objects.filter(course=course)
        lectureproblems = LectureProblem.objects.filter(lecture__in=lectures, problem__name__icontains=problem_name)
        for lectureproblem in lectureproblems:
            problem = lectureproblem.problem
            problems.append({
                'code': problem.code,
                'name': problem.name,
                'description': problem.description,
                'type': '练习题'
                })
                
        '''Now for labs'''
        labs = Lab.objects.filter(course=course)
        labproblems = LabProblem.objects.filter(lab__in=labs, problem__name__icontains=problem_name)
        for labproblem in labproblems:
            problem = labproblem.problem
            problems.append({
                'code': problem.code,
                'name': problem.name,
                'description': problem.description,
                'type': '实验题'
                })
                
        '''Now for exams'''
        exams = Exam.objects.filter(course=course)
        examproblems = ExamProblem.objects.filter(exam__in=exams, problem__name__icontains=problem_name)
        for examproblem in examproblems:
            problem = examproblem.problem
            problems.append({
                'code': problem.code,
                'name': problem.name,
                'description': problem.description,
                'type': '考试题'
                })
                
        paginator = Paginator(problems, page_length)
        problems = paginator.page(page)
        results = []
        for problem in problems:
            results.append(problem)
        return self.success({'problems':results,
            'totalPages':paginator.num_pages,
            'current': page,
            'all_problems': len(results)})