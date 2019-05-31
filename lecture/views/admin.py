from utils.api import APIView, JSONResponse
from django.http import StreamingHttpResponse
from lecture.models import Lecture, LectureProblem
from django.db import models
from course.models import Course, CourseResource
from lecture.serializers import LectureSerializers
from ..serializers import LectureSerializers, GetLectureSerializer
from problem.models import Problem
from django.views.decorators.http import require_http_methods
from django.shortcuts import render
from django.http import HttpResponse

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
                # lecture = Lecture.objects.get(id=lecture_id)
                for i in problem_ids:
                    id = i.problem_id
                    LP = LectureProblem.object.filter(lecture=lecture_id, problem=id)
                    if len(LP)<=0:
                        lp = LectureProblem(lecture=lecture_id, problem=id)
                        lp.save()
                        response_object['lecture_id'] = lecture_id
                        response_object['problem_ids'] = problem_ids
                        return self.success(response_object)
            except Exception as exception:
                return self.error(err=exception, msg=str(exception))

class EditLectureAPI(APIView):
    response_class = JSONResponse
    def post(self, request):
        response_object = dict()
        # get information from frontend
        try:
            lecture_id = int(request.POST.get('lecture_id'))
            name = request.POST.get('name')
            description = request.POST.get('description')
        except Exception as exception:
            return self.error(err=exception.args, msg="lecture_id:%s\n" % (request.POST.get('lecture_id')))
        try:
            # update lecture
            Lecture.objects.filter(id=lecture_id).update(name=name, description=description)

            #successful return
            response_object["state_code"] = 200
            return self.success(response_object)
        except Exception as exception:
            return self.error(err=exception.args, msg=str(exception))

class DeleteLectureAPI(APIView):
    response_class = JSONResponse
    def post(self, request):
        response_object = dict()
        # get information from frontend
        try:
            lecture_id = int(request.POST.get('lecture_id'))
        except Exception as exception:
            return self.error(err=exception.args, msg="lecture_id:%s\n" % ( request.POST.get('lecture_id') ) )
        try:
            # delete lecture
            lec=Lecture.objects.get(id=lecture_id)
            lec.delete()

            #successful return
            response_object["state_code"] = 200
            return self.success(response_object)
        except Exception as exception:
            return self.error(err=exception.args, msg=str(exception))


class AddFileAPI(APIView):
    response_class = JSONResponse
    def post(self, request):
        response_object = dict()
        # get information from frontend
        try:
            lecture_id = int(request.POST.get('lecture_id'))
            filename= request.POST.get('filename')
            file=request.POST.get('file')
        except Exception as exception:
            return self.error(err=exception.args, msg="lecture_id:%s, filename:%s, file:%s\n" % (request.POST.get('lecture_id'),request.POST.get('filename'),request.POST.get('file') ))
        try:
            # add course file
            lecture=Lecture.objects.get(id=lecture_id)

            course_resource=CourseResource(name=filename,file=file)
            course_resource.save()
            lecture.resources.add(course_resource)

            #successful return
            response_object["state_code"] = 200
            return self.success(response_object)
        except Exception as exception:
            return self.error(err=exception.args, msg=str(exception))

class DeleteProblems(APIView):
    response_class = JSONResponse
    def get(self, request):
        response_object = dict()
        # get information from frontend
        try:
            lecture_id = int(request.GET.get('lectureId'))
            problem_id = request.GET.get('problemId')
        except Exception as exception:
            return self.error(err=exception.args, msg="lecture_id:%s, problem_ids:%s\n"%(request.POST.get('lecture_id'), request.POST.get('problem_ids')))
        try:
            # delete imformation in database
            lecture = Lecture.objects.get(id=lecture_id)
            print(lecture)
            problem = Problem.objects.get(id=problem_id)
            print(problem)
            lecture.problems.remove(problem)

            response_object['success'] = 200
            return self.success(response_object)
        except Exception as exception:
            return self.error(err=exception, msg=str(exception))




class DeleteCourseResource(APIView):
    response_class = JSONResponse
    def get(self, request):
        print('test')
        response_object = dict()
        # get information from frontend
        try:
            print(request.GET)
            lecture_id = int(request.GET.get('lectureId'))
            file_id = request.GET.get('fileName')
            print(lecture_id)
            print(file_id)
        except Exception as exception:
            return self.error(err=exception.args, msg="lecture_id:%s, file_id:%s\n"%(request.POST.get('lecture_id'), request.POST.get('file_id')))
        try:
            # insert new problems into database
            lecture = Lecture.objects.get(id=lecture_id)
            resource = CourseResource.objects.get(id = file_id)
            print(lecture)
            print(resource)
            lecture.resources.remove(resource)
            #resource.delete()
            response_object['success'] = 200
            return self.success(response_object)
        except Exception as exception:
            return self.error(err=exception, msg=str(exception))



@require_http_methods(["POST"])
def file_download(request):
    try:
        resources_namelist = eval(list(request.POST.keys())[0])
        resources_name = resources_namelist["file_name"]
    except Exception as exception:
        errormsg=error(err=exception.args, msg="lecture_id:%s, resources_name:%s\n"%(request.POST.get('lecture_id'), request.POST.get('file_name')))
        response['error'] = errormsg
    def file_iterator(file_name, chunk_size=512):
        filepath = r'/mnt/d/lecture1.pdf' #实际使用时将路径改成文件所在的路径
        with open(filepath,'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    print(resources_name)
    resources = CourseResource.objects.get(file=resources_name)
    print(resources)
    the_file_name = resources.file.url
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)
    return response
