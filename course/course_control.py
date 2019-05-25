from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, JsonRequest
from .models import Course


@csrf_exempt
@require_http_methods(['POST'])
def delete_course(request):
    '''删除课程'''
    response = {}
    course_code = response.POST.get('courseCode')
    if not Course.objects.filter(code=course_code).exists():
        response['errorNum'] = CourseNotExists
    else:
        course = Course(code=course_code, deleted=True)
        course.save()
        response['errorNum'] = SUCCESS
    return JsonResponse(response)


@csrf_exempt
@require_http_methods(['POST'])
def duplicate_course(request):
    '''复制课程'''
    response = {}
    course_code = response.POST.get('courseCode')
    if not Course.objects.filter(code=course_code).exists():
        response['errorNum'] = CourseNotExists
    else:
        # 赋予复制后的课程新code并返回该code，新课其余信息与原课一致
        codes = [int(course.code) for course in Course().objects]
        new_course_code = str(max(codes)+1)
        course = Course(code=course_code)
        Course.objects.create(code=new_course_code, name=course.name,
                              start_time=course.start_time, end_time=course.end_time,
                              description=course.description, deleted=course.deleted,
                              students=course.students, teachers=course.teachers)
        response['errorNum'] = SUCCESS
        response['newCourseID'] = new_course_code
    return JsonResponse(response)
