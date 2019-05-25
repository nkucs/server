from .models import Course, CourseTeacher
from ../models/user import Teacher
from django.http import JsonResponse, JsonRequest

@csrf_exempt
@require_http_methods(['POST'])
def add_course(request):
    response = {}
    teacher_number = request.POST.get('teacherNumber')
    name = request.POST.get('name')
    start_time = request.POST.get('startTime')
    end_time = request.POST.get('endTime')
    description = request.POST.get('description')
    teacher = Teacher.objects.filter(teacher_number=teacher_number)
    Course.objects.create_course(course_name=name,
                                 start_time=start_time,
                                 end_time=end_time,
                                 description=description)
    response['errorNum'] = SUCCESS
    return JsonResponse(response)



def create_course(self, course_name, start_time, end_time, description):
    course = self.model(
        course.name = course_name,
        course.start_time = start_time,
        course.end_time = end_time,
        course.description = description
    )
    course.save()
    return course


@csrf_exempt
@require_http_methods(['POST'])
def update_course(request):
    response = {}
    teacher_number = request.POST.get('teacherNumber')
    name = request.POST.get('name')
    start_time = request.POST.get('startTime')
    end_time = request.POST.get('endTime')
    description = request.POST.get('description')
    teacher = Teacher.objects.filter(teacher_number=teacher_number)
    course = Course.objects
    course.name = name
    course.start_time = start_time
    course.end_time = end_time
    course.description = description
    response['errorNum'] = SUCCESS
    return JsonResponse(response)