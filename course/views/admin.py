from utils.api import APIView, JSONResponse
from django.http import HttpResponse, JsonResponse
from django.db import models
from course.models import Course


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
