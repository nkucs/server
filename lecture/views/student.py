from utils.api import APIView, JSONResponse
from lecture.models import Lecture
from django.db import models
from course.models import Course, LectureResource
from lecture.serializers import LectureSerializers
from ..serializers import LectureSerializers, GetLectureSerializer
from problem.models import Problem
from problem.models import Case
from submission.models import ProblemSubmission, ProblemSubmissionCase
from django.http import FileResponse


def select_lecture_bycourse(course):
    lecture_list = set()
    lectures=Lecture.objects.filter(course=course)
    for lecture in lectures:
        lecture_list.add(lecture)
    return lecture_list

def select_resource_bylectureid(lecture_id):
    resource_list = set()
    resources=LectureResource.objects.filter(lecture_id=lecture_id)
    for resource in resources:
        resource_list.add(resource)
    return resource_list

def select_lecture_byname(name):
    lecture_list = set()
    lectures=Lecture.objects.filter(name=name)
    for lecture in lectures:
        lecture_list.add(lecture)
    return lecture_list


class ShowLecture(APIView):
    response_class = JSONResponse
    def get(self, request):
        response_object = dict()
        # get information from frontend
        try:
            course_id = int(request.GET.get('course_id'))
        except Exception as exception:
            return self.error(err=exception.args, msg="course_id:%s\n"%(request.POST.get('course_id')))
        try:
            # return lectures to the frontend
            lecture_list=list(select_lecture_bycourse(course_id))
            for i in range(len(lecture_list)):
                response_object['key']=lecture_list[i].id
                response_object['name']=lecture_list[i].name
                response_object["source"]=lecture_list[i].resources.all()
                print(response_object)
            return self.success(response_object)
        except Exception as exception:
            return self.error(err=exception, msg=str(exception))

class ShowLectureName(APIView):
    response_class = JSONResponse
    def get(self, request):
        response_object = dict()
        # get information from frontend
        try:
            name = request.GET.get('name')
        except Exception as exception:
            return self.error(err=exception.args, msg="name:%s\n"%(request.POST.get('name')))
        try:
            # return lectures to the frontend
            lecture_list=list(select_lecture_byname(name))
            for i in range(len(lecture_list)):
                response_object['key']=i+1
                response_object['name']=lecture_list[i].name
                response_object["source"]=lecture_list[i].resources.all()
                print(response_object)
            return self.success(response_object)
        except Exception as exception:
            return self.error(err=exception, msg=str(exception))

class ShowMyLecturesAPI(APIView):
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

class DownloadSourseById(APIView):
    response_class = JSONResponse
    def get(self, request):
        # initialize the response object
        response_object = dict()
        # get information from frontend
        try:
            page = int(request.GET.get('page'))
            course_id = int(request.GET.get('course_id'))
            page_length = int(request.GET.get('page_length'))
            sourse_id = request.GET.get('sourse_id')
        except Exception as exception:
            return self.error(err=exception.args, msg="course_id:%s, page:%s\n"%(request.GET.get('course_id'), request.GET.get('page')))
        try:
            file=open('/home/amarsoft/下载/example.tar.gz','rb')
            response =FileResponse(file)
            response['Content-Type']='application/octet-stream'
            response['Content-Disposition']='attachment;filename="example.tar.gz"'
            return self.success(response)
        except Exception as exception:
            return self.error(err=exception.args, msg=str(exception))

class LectureProblem (APIView):
    response_class = JSONResponse

    def get(self, request):
        response_object = dict()
    # get information from frontend
        try:
            course_id = int(request.GET.get("course_id"))
            page = int(request.GET.get("page"))
            page_length = int(request.GET.get("page_length"))
        except Exception as exception:
            return self.error(err=exception.args,
                              msg="problem_id:%s, name:%s, description:%s\n" % (request.GET.get('problem_id')))
    # get data from database
        try:
            query_set = LectureProblem.objects.filter(lectuer=course_id)
            problem_count = query_set.count()
            if problem_count == 0:
                response_object['total_counts'] = problem_count
                return self.success(response_object)
            problem_id_list = query_set[(page - 1) * page_length: page * page_length].values("problem", "language")
            problem_list = []
            for problem_id in problem_id_list:
                query_set_problem = Problem.objects.filter(id=problem_id["problem"])
                problem_list.append(query_set_problem)
                problem_list["language"] = problem_id["language"]
            response_object['total_counts'] = problem_count
            response_object['problem_list'] = LectureSerializers(problem_list, many=True).data
            return self.success(response_object)
        except Exception as exception:
            return self.error(err=exception.args, msg=str(exception))

class GetAllMessage(APIView):
    def get(self, request):
        results = []
        try:
            allMessage = Message.objects.all()
            result = [{
					'content': '第1次作业提交时间将要截止',
					'course_name': '数据结构',
				},{
					'content': '第2次作业提交时间将要截止',
					'course_name': '数据结构',
				},{
					'content': '第3次作业提交时间将要截止',
					'course_name': '数据结构',
				},{
					'content': '第4次作业提交时间将要截止',
					'course_name': '数据结构',
				}]
            for message in allMessage :
                content = message.content
                courseName = message.course.name
                results.append({
                    'content' : content,
                    'course_name' : courseName
                })
            return self.success(result)
        except Exception as e:
            # not found
            return self.error(msg=str(e), err=e.args)