from ..models import Problem
from ..serializers import GetProblemSerializer,GetProblemsSerializer,GetOneProblemSerializer
from ..serializers import ProblemSubmissionTimeSerializers,ProblemSubmission,ProblemSubmissionCase,GetTeacherSerializer,GetCasesSerializer,GetTagsSerializer
from ..models import Problem
from utils.api import APIView, JSONResponse
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from problem.models import Problem,Tag,Case
from user.models import Teacher
from django.db import models
import random
import json

class GetProblemAPI(APIView):
    """get one problem  
        by problem_id
    """
    def get(self, request):
        problem_id = int(request.GET.get('problem_id'))
        cases = []
        # query from database
        try:
            problem = Problem.objects.get(id=problem_id)
            cases_number = Case.objects.filter(problem=problem_id).count()
            cases_list = Case.objects.filter(problem=problem_id)
            for i in range(cases_number):
                case = cases_list[i]
                cases_serializer= GetCasesSerializer(case).data
                cases.append(cases_serializer)
            problem.cases = cases
        except Problem.DoesNotExist:
            return HttpResponse(status=404)
        serializer = GetProblemSerializer(problem)
        return JsonResponse(serializer.data,status=status.HTTP_200_OK)

    
class GetSubmissionsAPI(APIView):
    def get(self, request):
        list_count = 10
        # initialize the response object
        response_object = dict()
        problemSubmission = []
        page = int(request.GET.get('page'))
        problem_id = int(request.GET.get('problem_id'))
        # query from database
        try:
            problemSubmission_number = ProblemSubmission.objects.filter(problem_id=problem_id).count()
            problemSubmission_list = ProblemSubmission.objects.filter(problem_id=problem_id)
            for i in range(problemSubmission_number):
                problemSubmission_one = problemSubmission_list[i]
                problemSubmission_one.student_number = problemSubmission_one.student.student_number
                problemSubmission_one.all_cases_count = problemSubmission_one.cases.count()
                problemSubmissionCase_number =ProblemSubmissionCase.objects.filter(problem_submission=problemSubmission_one.id).count()
                problemSubmissionCase =ProblemSubmissionCase.objects.filter(problem_submission=problemSubmission_one.id)
                problemSubmission_one.succeed_cases_count = 0
                for j in range(problemSubmissionCase_number):
                    problemSubmissionCase_one = problemSubmissionCase[j]
                    if problemSubmissionCase_one.case_status.name in ['AC','ac']:
                        problemSubmission_one.succeed_cases_count += 1
                serializer = ProblemSubmissionTimeSerializers(problemSubmission_one).data
                problemSubmission.append(serializer) 
            # update response object
        except ProblemSubmission.DoesNotExist:
            return HttpResponse(status=404)
        response_object['total_pages'] = problemSubmission_number // list_count + 1
        response_object['current_page'] = page
        response_object['submissions'] = problemSubmission
        return JsonResponse(response_object,status=status.HTTP_200_OK)


class CreateProblemAPI(APIView):
    # response to post request
    def get(self,request):
        # response_object = dict()
        # get information from frontend
        # try:
        problem_name = request.GET.get('problem_name')
        description = request.GET.get('description')
        created_teacher_id = int(request.GET.get('created_teacher_id'))
        runtime_limit = int(request.GET.get('runtime_limit'))
        memory_limit = int(request.GET.get('memory_limit'))
        problem_tags = request.GET.getlist('tags[]')
        cases = request.GET.getlist('cases[]')
        # except Exception as exception:
        #      # return self.error(err=exception.args, msg="problem_name:%s, description:%s, created_teacher_id:%s,runtime_limit:%s,memory_limit:%s\n"%(request.GET.get('problem_name'), request.GET.get('description'), request.GET.get('created_teacher_id'), request.GET.get('runtime_limit'), request.GET.get('memory_limit')))
        #      return HttpResponse('error1')
        # insert new problem and cases to database
            # find teacher from Teacher table
        teacher = Teacher.objects.get(id=created_teacher_id)
            # add problem to  problem table
        rand_code = random.random()
        problem = Problem.objects.create(code=str(rand_code), name=problem_name,description=description,teacher=teacher,runtime_limit=runtime_limit,memory_limit=memory_limit)
            # response_object['problem_id'] = problem.id
        teacher_ser = GetTeacherSerializer(teacher)
            # add problem_tags

        for problem_tag in problem_tags:
            tag = Tag.objects.get(name=problem_tag)
            problem.tags.add(tag) # add tag to problem
        problem_ser =GetOneProblemSerializer(problem)
        # add cases to case table 
        for i in range(len(cases)):
            case = json.loads(cases[i])
            case_input = case["input"]
            case_output = case["output"]
            case_type = int(case["type"]) # zero for test, one for example
            weight = case["weight"]
            # case_tags = case.tags
            # create case in Case  table
            case = Case.objects.create(input=case_input,output=case_output,type=case_type,problem=problem,weight=weight)
            # add case_tags
            # for case_tag in case_tags:
            #     tag = Tag.objects.get(name=case_tag)
            #     case.tags.add(tag)  # add tag to case
        return JsonResponse(problem_ser.data)
    


class EditProblemAPI(APIView):
    # response to post request
    def get(self,request):
        # response_object = dict()
        # get information from frontend
        # try:
        problem_id = request.GET.get("problem_id")
        problem_name = request.GET.get('problem_name')
        description = request.GET.get('description')
        created_teacher_id = int(request.GET.get('created_teacher_id'))
        runtime_limit = int(request.GET.get('runtime_limit'))
        memory_limit = int(request.GET.get('memory_limit'))
        problem_tags = request.GET.getlist('tags[]')
        cases = request.GET.getlist('cases[]')
        # except Exception as exception:
        #      return self.error(err=exception.args, msg="problem_id:%s, problem_name:%s, description:%s, created_teacher_id:%s,runtime_limit:%s,memory_limit:%s\n"%(request.POST.get('problem_id'),request.POST.get('problem_name'), request.POST.get('description'), request.POST.get('created_teacher_id'), request.POST.get('runtime_limit'), request.POST.get('memory_limit')))
        #  update the problem information
        # try:
        # find the teacher
        teacher = Teacher.objects.get(id=created_teacher_id)
        # obtain the problem by id
        problem = Problem.objects.get(id=int(problem_id))
        # update the problem
        Problem.objects.filter(id=int(problem_id)).update(name=problem_name,description=description,teacher=teacher,runtime_limit=runtime_limit,memory_limit=memory_limit)
        # response_object['problem_id'] = problem.id

        # change the problem tags
        # clear all old tags
        problem.tags.clear()
        # add new tags
        for problem_tag in problem_tags:
            tag = Tag.objects.get(name=problem_tag)
            problem.tags.add(tag)

        # change the problem cases
        # delete old cases
        old_cases = problem.case_set.all()
        for old_case in old_cases:
            # old_case.tags.clear()
            old_case.delete()
        # add new cases
        for case in cases:
            case = json.loads(case)
            case_input = case["input"]
            case_output = case["output"]
            case_type = case["type"] # zero for test, one for example
            weight = case["weight"]
            case_tags = case["tags"]
            # create case in Case  table
            case = Case.objects.create(input=case_input,output=case_output,type=case_type,problem=problem,weight=weight)
            # add case_tags
            # for case_tag in case_tags:
            #     tag = Tag.objects.get(name=case_tag)
            #     case.tags.add(tag) 
        problem_ser =GetOneProblemSerializer(problem)
        return JsonResponse(problem_ser.data)
        # except Exception as exception:
        #     return self.error(err=exception, msg=str(exception))
    


class DeleteProblemAPI(APIView):
    def get(self, request):
        try:
            problem_id = int(request.GET.get('problem_id'))
            Problem.objects.get(id=problem_id).delete()
        except Exception as exception:
            return self.error(err=exception.args, msg="problem_id: %s"%(request.POST.get('problem_id')))
        else:
            return self.success({'msg': 'success'})


class AddTagAPI(APIView):
    def post(self,request):
        response_object = dict()
        try:
            # get tag name
            name = request.POST.get('tag_name')
            # add tag to Tag table
            tag = Tag.objects.create(name=name)
            response_object['tag_id'] = tag.id
        except Exception as exception:
            return self.error(err=exception.args, msg="tag_name: %s"%(request.POST.get('tag_name')))
        else:
            return self.success(response_object)

class GetProblemsAPI(APIView):
    response_class = JSONResponse
    def get(self, request):
        response_object = dict()
        try:
            current_page = int(request.GET.get('page'))
        except Exception as exception:
            return self.error(err=exception.args, msg="No page")
        
        try:
            # query from database
            problem_list = Problem.objects.all()
            
            # update response object
            response_object['total_pages'] = 10
            response_object['current_page'] = current_page
            response_object['problems'] = GetProblemsSerializer(problem_list, many=True).data

            return self.success(response_object)
        except Exception as exception:
            return self.error(err=exception.args, msg=str(exception))
