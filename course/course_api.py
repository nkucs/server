from .models import Course, CourseTeacher
from user.models import Teacher
from django.http import JsonResponse
from django.core.paginator import Paginator , PageNotAnInteger,EmptyPage


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

def get_all_course(request):
    response = dict()
    page_length = request.GET.get('pageLength')
    page = request.GET.get('page')
    teacher = request.GET.get('teacher')
    name = request.GET.get('name')
    courses = get_course_all()
    if teacher != '':
        course_list_by_teacher = select_course_by_teacher(teacher)
        courses = courses.intersection(course_list_by_teacher)
    if name != '':
        course_list_by_name = select_course_by_name(name)
        courses = courses.intersection(course_list_by_name)
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
    response['courses'] = get_course_info(courses)
    response['errorNum'] = SUCCESS
    return JsonResponse(response)
    
def get_my_course(request):
    response = dict()
    teacher_number = request.GET.get('teacherNumber')
    page_length = request.GET.get('pageLength')
    page = request.GET.get('page')
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
    response['courses'] = get_course_info(courses)
    response['errorNum'] = SUCCESS
    return JsonResponse(response)
