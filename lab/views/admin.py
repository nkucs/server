from course.models import Course, CourseResource
from problem.models import Problem
from utils.api import APIView, JSONResponse, FILEResponse
from ..serializers import LabSerializers, GetLabSerializer, GetProblemsSerializer, GetLabProblemsSerializer
from ..models import Lab, LabProblem
import datetime


class FilterProblemsAPI(APIView):
    response_class = JSONResponse
    def get(self, request):
        list_count = 6
        response_object = dict()
        try:
            code = request.GET.get('code')
            page = int(request.GET.get('page'))
            tag_name = request.GET.get('tag_name')
            problem_name = request.GET.get('problem_name')
            teacher_name = request.GET.get('teacher_name')
        except Exception as exception:
            return self.error(err=exception.args,
                              msg="page:%s, tag_name:%s, code: %s, problem_name: %s\n" % (request.GET.get('page'), request.GET.get('tag_name'), request.GET.get('code'),request.GET.get('problem_name'),))
        try:
            if code != '':
                query_result = Problem.objects.filter(code=code)
            else:
                query_result = Problem.objects.filter(name__icontains=problem_name)\
                    .filter(tags__name__icontains=tag_name)\
                    .filter(teacher__user__name__icontains=teacher_name)
            teacher_name_list = list()
            tag_name_list = list()
            for prob in query_result:
                teacher_name_list.append(prob.teacher.user.name)
                tag_name_list.append([tag.name for tag in prob.tags.all()])

            problems_count = query_result.count()
            problems_list = query_result[(page-1) * list_count: page * list_count]
            teacher_name_list = teacher_name_list[(page-1) * list_count: page * list_count]
            tag_name_list = tag_name_list[(page-1) * list_count: page * list_count]
            response_object['total_pages'] = problems_count // list_count + 1
            response_object['current_page'] = page
            response_object['teacher_names'] = teacher_name_list
            response_object['tag_names'] = tag_name_list
            response_object['problems'] = GetProblemsSerializer(problems_list, many=True).data
            return self.success(response_object)
        except Exception as exception:
            return self.error(err=exception.args, msg=str(exception))


class GetProblemsAPI(APIView):
    '''
    根据实验id 获取与该实验关联的所有题目
    GET 方法
    '''
    response_class = JSONResponse
    def get(self, request):
        response_object = dict()
        try:
            lab_id = int(request.GET.get('lab_id'))
        except Exception as exception:
            return self.error(err=exception.args,
                              msg="lab_id:%s \n" % (request.GET.get('lab_id')))
        try:
            lab = Lab.objects.get(id=lab_id)
            problems = LabProblem.objects.filter(lab=lab)
            response_object['problems'] = GetLabProblemsSerializer(problems, many=True).data
            return self.success(response_object)
        except Exception as exception:
            return self.error(err=exception.args, msg=str(exception))


class CreateLabAPI(APIView):
    response_class = JSONResponse
    def post(self, request):
        response_object = dict()
        # get information from frontend
        try:
            course_id = int(request.data['course_id'])
            name = request.data['name']
            description = request.data['description']
            start_time = request.data['start_time']
            end_time = request.data['end_time']
            attachment_weight = int(request.data['attachment_weight'])
            report_required = request.data['report_required']
            problems = request.data['problems']
            problems_code_list = [pro['id'] for pro in problems]

            if report_required == 'y':
                report_required = True
            else:
                report_required = False

            start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
            end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')

        except Exception as exception:
            return self.error(err=exception.args, msg="course_id:%s, name:%s, description:%s\n"%
                (request.POST.get('course_id'), request.POST.get('name'), request.POST.get('description')))

        try:
            course = Course.objects.get(id=course_id)
            lab = Lab.objects.create(
                course=course,
                name=name,
                description=description,
                start_time=start_time,
                end_time=end_time,
                attachment_weight=attachment_weight,
                problem_weight=100 - attachment_weight,
                report_required=report_required
            )
            print(lab)
            response_object['lab_id'] = lab.id

            # 然后为每个练习题建立一个 lab_problem 的条目
            try:
                lab_problems =  LabProblem.objects.all()
                print(lab_problems.values())

                for code in problems_code_list:
                    problem = Problem.objects.get(code=code)
                    lab_problem = LabProblem.objects.create(
                        lab=lab,
                        problem=problem,
                        weight=100-attachment_weight,
                        language=63)
                return self.success(response_object)
            except Exception as exception:
                return self.error(err=exception, msg=str(exception))
        except Exception as exception:
            return self.error(err=exception, msg=str(exception))


class EditLabAPI(APIView):
    response_class = JSONResponse
    def post(self, request):
        response_object = dict()
        try:
            lab_id = int(request.data['lab_id'])
            name = request.data['name']
            description = request.data['description']
            start_time = request.data['start_time']
            end_time = request.data['end_time']
            attachment_weight = int(request.data['attachment_weight'])
            report_required = request.data['report_required']
            problems = request.data['problems']

            if report_required == 'y':
                report_required = True
            else:
                report_required = False

            start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
            end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')

        except Exception as exception:
            return self.error(err=exception.args, msg="lab_id:%s, name:%s, description:%s\n"%
                (request.data['lab_id'], request.data['name'], request.data['description']))
        try:
            Lab.objects.filter(id=lab_id).update(
                name=name,
                description=description,
                start_time=start_time,
                end_time=end_time,
                attachment_weight=attachment_weight,
                problem_weight=100 - attachment_weight,
                report_required=report_required
            )
            response_object["state_code"] = 200
            return self.success(response_object)
        except Exception as exception:
            return self.error(err=exception, msg=str(exception))


class GetLabsAPI(APIView):
    response_class = JSONResponse
    def get(self, request):
        # suppose that one page contains 10 lab information
        list_count = 10
        # initialize the response object
        response_object = dict()
        # get information from frontend
        try:
            course_id = int(request.GET.get('course_id'))
            page = int(request.GET.get('page'))
        except Exception as exception:
            return self.error(err=exception.args, msg="course_id:%s, page:%s\n"%(request.GET.get('course_id'), request.GET.get('page')))
        
        try:
            # query from database
            labs_number = Lab.objects.filter(course=course_id).count()
            labs_list = Lab.objects.filter(course=course_id)[(page - 1) * list_count : page * list_count].values('id', 'name', 'start_time', 'end_time')
            # update response object
            response_object['total_pages'] = labs_number // list_count + 1
            response_object['current_page'] = page
            response_object['labs'] = LabSerializers(labs_list, many=True).data

            return self.success(response_object)
        except Exception as exception:
            return self.error(err=exception.args, msg=str(exception))


class DeleteLabAPI(APIView):
    def post(self, request):
        try:
            lab_id = int(request.POST.get('lab_id'))
            Lab.objects.get(id=lab_id).delete()
        except Exception as e:
            return self.error(err=e.args, msg="lab_id: %s"%(request.POST.get('lab_id')))
        else:
            return self.success({'msg': 'success'})

class GetSubmissionFileAPI(APIView):
    """
    Get a file of a lab.
    API: get-submission-file
    """

    response_class = FILEResponse

    def get(self, request):
        attachment_id = request.GET.get('attachment_id')
        # check if attachment_id exists
        if not attachment_id:
            # not found
            return self.error(msg=f'key "attachment_id" is None', err=request.GET)
        try:
            # query for the lab
            course_resource = CourseResource.objects.get(id=attachment_id)
            return FILEResponse.response(course_resource.file)
        except Exception as e:
            # not found
            return self.error(msg=str(e), err=e.args)

class GetLabAPI(APIView):
    """
    Get data of a lab.
    API: get-lab
    """
    response_class = JSONResponse

    def get(self, request):
        lab_id = request.query_params['lab_id']
        # check if lab_id exists
        if not lab_id:
            #not found
            return self.error(msg=f"lab_id key is None", err=request.GET)
        try:
            # query for the lab
            lab_object = Lab.objects.get(id=lab_id)
            print(lab_object)
            return self.success(GetLabSerializer(lab_object).data)
        except Exception as e:
            # not found
            return self.error(msg=str(e), err=e.args)
