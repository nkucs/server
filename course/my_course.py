from .models import Course, CourseTeacher
from user.models import Teacher
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import datetime


@require_http_methods(['GET'])
def get_course_details(course):
    course_details = dict()
    course_details['course_id'] = course.code
    course_details['name'] = course.name
    course_details['start_time'] = course.start_time
    course_details['end_time'] = course.end_time
    course_details['description'] = course.description
    return course_details


@require_http_methods(['GET'])
def get_my_current_course(request):
    response = dict()
    teacher_number = request.GET.get('teacherNumber')
    teacher = Teacher.objects.get(teacher_number=teacher_number)
    courses_teacher = CourseTeacher.objects.filter(teacher=teacher)
    courses = list()
    cur_time = datetime.date.today()
    for course_teacher in courses_teacher:
        cur_course = course_teacher.course
        s_time = cur_course.start_time
        e_time = cur_course.end_time
        if cur_time.__le__(e_time) and cur_time.__ge__(s_time): 
            courses.append(get_course_details(cur_course))
    response['courses'] = courses
    response['errorNum'] = SUCCESS
    return JsonResponse(response)
