from utils.api import APIView, JSONResponse
from lecture.models import Lecture
from django.db import models
from course.models import Course
class CreateLectureAPI(APIView):
    response_class = JSONResponse
    def post(self, request):
        response_object = dict()
        # get information from frontend
        try:
            course_id = int(request.POST.get('course_id'))
            name = request.POST.get('name')
            description = request.POST.get('description')
        except Exception as exception:
            return self.error(err=exception.args, msg="course_id:%s, name:%s, description:%s\n"%(request.POST.get('course_id'), request.POST.get('name'), request.POST.get('description')))
        try:
            # insert new lecture into database
            course = Course.objects.get(id=course_id)
            lecture = Lecture.objects.create(course=course, name=name, description=description)
            response_object['lecture_id'] = lecture.id
            return self.success(response_object)
        except Exception as exception:
            return self.error(err=exception, msg=str(exception))
