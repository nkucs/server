from utils.api import APIView, JSONResponse
from django.http import StreamingHttpResponse
from lecture.models import Lecture, LectureProblem
from django.db import models
from course.models import Course, CourseResource
from lecture.serializers import LectureSerializers
from ..serializers import LectureSerializers, GetLectureSerializer
from problem.models import Problem

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

class EditProblems(APIView):
    response_class = JSONResponse
    def post(self, request):
        response_object = dict()
        # get information from frontend
        try:
            lecture_id = int(request.POST.get('lecture_id'))
            problem_ids = request.POST.get('problem_ids')
        except Exception as exception:
            return self.error(err=exception.args, msg="lecture_id:%s, problem_ids:%s\n"%(request.POST.get('lecture_id'), request.POST.get('problem_ids')))
        try:
            # insert new problems into database
            lecture = Lecture.objects.get(id=lecture_id)
            for i in problem_ids:
                problem = Problem.objects.get(id=i.problem_id)
                lecture.problems.add(problem)
                lp = LectureProblem(lecture=lecture, problem=problem)
                lp.save()

            response_object['lecture_id'] = lecture.id
            response_object['problem_ids'] = lecture.problems
            return self.success(response_object)
        except Exception as exception:
            return self.error(err=exception, msg=str(exception))

class DeleteProblems(APIView):
    response_class = JSONResponse
    def post(self, request):
        response_object = dict()
        # get information from frontend
        try:
            lecture_id = int(request.POST.get('lecture_id'))
            problem_ids = request.POST.get('problem_ids')
        except Exception as exception:
            return self.error(err=exception.args, msg="lecture_id:%s, problem_ids:%s\n"%(request.POST.get('lecture_id'), request.POST.get('problem_ids')))
        try:
            # delete imformation in database
            lecture = Lecture.objects.get(id=lecture_id)
            for i in problem_ids:
                problem = Problem.objects.get(id=i.problem_id)
                lp = LectureProblem.objects.filter(lecture=lecture, problem=problem)
                lp.delete()
                lecture.problems.delete(problem)

            response_object['success'] = 200
            return self.success(response_object)
        except Exception as exception:
            return self.error(err=exception, msg=str(exception))

class DeleteCourseResource(APIView):
    response_class = JSONResponse
    def post(self, request):
        response_object = dict()
        # get information from frontend
        try:
            lecture_id = int(request.POST.get('lecture_id'))
            resources_name = request.POST.get('file_name')
        except Exception as exception:
            return self.error(err=exception.args, msg="lecture_id:%s, resources_name:%s\n"%(request.POST.get('lecture_id'), request.POST.get('file_name')))
        try:
            # insert new problems into database
            resources = CourseResource.objects.get(name=file_name)
            resource = resources.lectures.get(id=lecture_id)
            lecture = Lecture.objects.get(id=lecture_id)
            lecture.remove(resource)
            resource.delete()
            response_object['success'] = 200
            return self.success(response_object)
        except Exception as exception:
            return self.error(err=exception, msg=str(exception))




def file_download(request):
    try:
        lecture_id = int(request.POST.get('lecture_id'))
        resources_name = request.POST.get('file_name')
    except Exception as exception:
        errormsg=error(err=exception.args, msg="lecture_id:%s, resources_name:%s\n"%(request.POST.get('lecture_id'), request.POST.get('file_name')))
        response['error'] = errormsg
    def file_iterator(file_name, chunk_size=512):
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    resources = CourseResource.objects.get(name=file_name)
    resource = resources.lectures.get(id=lecture_id)
    the_file_name = resource.file
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response
