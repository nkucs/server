from utils.api import APIView, JSONResponse
from lecture.models import Lecture
from django.db import models
from course.models import Course
from lecture.serializers import LectureSerializers
from ..serializers import LectureSerializers, GetLectureSerializer

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


class GetMyLecturesAPI(APIView):
    response_class = JSONResponse
    def get(self, request):
        # initialize the response object
        response_object = dict()
        # get information from frontend
        try:
            page = int(request.GET.get('page'))
            course_id = int(request.GET.get('course_id'))
            page_length = int(request.GET.get('page_length'))
        except Exception as exception:
            return self.error(err=exception.args, msg="course_id:%s, page:%s\n"%(request.GET.get('course_id'), request.GET.get('page')))
        try:
            # query from database
            lectures_amount = Lecture.objects.filter(course=course_id).count()
            lectures_list = Lecture.objects.filter(course=course_id)[(page - 1) * page_length : page * page_length].values('id', 'name')
            response_object['total_counts'] = lectures_amount
            response_object['lectures'] = LectureSerializers(lectures_list, many=True).data
            return self.success(response_object)
        except Exception as exception:
            return self.error(err=exception.args, msg=str(exception))


class GetLectureAPI(APIView):
    response_class = JSONResponse

    def get(self, request):
        lecture_id = request.GET.get('lecture_id')
        if not lecture_id:
            #not found
            return self.error(msg=f"lecture_id key is None", err=request.GET)
        try:
            # query for the lecture
            lecture_object = Lecture.objects.get(id=lecture_id)
            return self.success(GetLectureSerializer(lecture_object).data)
        except Exception as e:
            # not found
            return self.error(msg=str(e), err=e.args)
