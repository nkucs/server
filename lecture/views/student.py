from django.forms import model_to_dict
from django.http import FileResponse
from course.models import Message
from problem.models import Problem
from lecture.models import LectureProblem, Lecture
from utils.api import APIView, JSONResponse


class LectureProblemAPI (APIView):
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
                              msg="problem_id:%s, name:%s, description:%s\n" % (request.GET.get('course_id')))
    # get data from database
        try:
            query_set = LectureProblem.objects.filter(lecture=course_id)
            problem_count = query_set.count()
            if problem_count == 0:
                response_object['total_counts'] = problem_count
                return self.success(response_object)
            problem_id_list = query_set[(page - 1) * page_length: page * page_length].values("problem", "language")
            problem_list = []
            data = dict()
            key = 0
            for problem_id in problem_id_list:
                query_set_problem = Problem.objects.get(id=int(problem_id["problem"]))
                t_data = model_to_dict(query_set_problem)
                response_object["name"] = t_data["name"]
                response_object["language"] = int(problem_id["language"])
                response_object["problem_id"] = int(problem_id["problem"])
                key += 1
                response_object["key"] = key
                problem_list.append(data)
            response_object['total_counts'] = problem_count
            #response_object['problem_list'] = problem_list
            return self.success(response_object)
        except Exception as exception:
            return self.error(err=exception.args, msg=str(exception))


def select_lecture_bycourse(course):
    lecture_list = set()
    lectures = Lecture.objects.filter(course=course)
    for lecture in lectures:
        lecture_list.add(lecture)
    return lecture_list

class ShowLecture(APIView):
    response_class = JSONResponse

    def select_lecture_bycourse(self, course):
        lecture_list = set()
        lectures = Lecture.objects.filter(course=course)
        for lecture in lectures:
            lecture_list.add(lecture)
        return lecture_list

    def get(self, request):
        response_object = dict()
        # get information from frontend
        try:
            course_id = int(request.GET.get('course_id'))
        except Exception as exception:
            return self.error(err=exception.args, msg="course_id:%s\n"%(request.POST.get('course_id')))
        try:
            # return lectures to the frontend
            lecture_list = list(select_lecture_bycourse(course_id))
            print(lecture_list)
            lecture_ppt = []
            for i in range(len(lecture_list)):
                print(lecture_list[i].id)
                response_object['key'] = lecture_list[i].id
                response_object['name'] = lecture_list[i].name
                querysets = lecture_list[i].resources.all()
                for one in querysets:
                    one = model_to_dict(one)
                    one.pop("file")
                    lecture_ppt.append(one)
                response_object['source'] = lecture_ppt
            print(response_object)
            return self.success(response_object)
        except Exception as exception:
            return self.error(err=exception, msg=str(exception))


def select_lecture_byname(name):
    lecture_list = set()
    lectures = Lecture.objects.filter(name=name)
    for lecture in lectures:
        lecture_list.add(lecture)
    return lecture_list


class ShowLectureName(APIView):
    response_class = JSONResponse

    def get(self, request):
        response_object = dict()
        # get information from frontend
        try:
            name = request.GET.get('name')
        except Exception as exception:
            return self.error(err=exception.args, msg="name:%s\n" % (request.GET.get('name')))
        try:
            # return lectures to the frontend
            lecture_list = list(select_lecture_byname(name))
            for i in range(len(lecture_list)):
                response_object['key'] = i+1
                response_object['name'] = lecture_list[i].name
                querysets = lecture_list[i].resources.all()
                lecture_ppt = []
                for one in querysets:
                    one = model_to_dict(one)
                    one.pop("file")
                    lecture_ppt.append(one)
                response_object['source'] = lecture_ppt
                print(response_object)
            return self.success(response_object)
        except Exception as exception:
            return self.error(err=exception, msg=str(exception))

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
            source_id = request.GET.get('source_id')
        except Exception as exception:
            return self.error(err=exception.args, msg="course_id:%s, page:%s\n" % (request.GET.get('course_id'), request.GET.get('page')))
        try:
            file = open('/home/amarsoft/下载/example.tar.gz', 'rb')
            response = FileResponse(file)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="example.tar.gz"'
            return self.success(response)
        except Exception as exception:
            return self.error(err=exception.args, msg=str(exception))

class GetAllMessage(APIView):
    def get(self, request):
        course_id = request.GET.get('course_id')
        if not course_id:
            #not found
            return self.error(msg=f"course_id key is None", err=request.GET)
        results = []    
        try:
            allMessage = Message.objects.filter(course_id=course_id)
            
            for message in allMessage :
                content = message.content
                courseName = message.course.name
                results.append({
                    'content' : content,
                    'course_name' : courseName
                })
            return self.success(results)
        except Exception as e:
            # not found
            return self.error(msg=str(e), err=e.args)

