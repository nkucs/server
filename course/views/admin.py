from utils.api import APIView, JSONResponse
from django.http import HttpResponse, JsonResponse
from django.db import models
from user.models import Teacher, User
from course.models import CourseTeacher, Course
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

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


class GetAllCourseAPI(APIView):
    response_class = JSONResponse
    def post(self, request):
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
    def post(self, request):
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

