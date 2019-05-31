from utils.api import APIView,JSONResponse
from problem.models import Problem,Tag,Case
from user.models import Teacher
from django.db import models

class CreateProblemAPI(APIView):
    # response to post request
    def post(self,request):
        response_object = dict()
        # get information from frontend
        try:
            problem_name = request.POST.get('problem_name')
            description = request.POST.get('description')
            created_teacher_id = request.POST.get('created_teacher_id')
            runtime_limit = request.POST.get('runtime_limit')
            memory_limit = request.POST.get('memory_limit')
            problem_tags = request.POST.get('tags')
            cases = request.POST.get('cases')
        except Exception as exception:
             return self.error(err=exception.args, msg="problem_name:%s, description:%s, created_teacher_id:%s,runtime_limit:%s,memory_limit:%s\n"%(request.POST.get('problem_name'), request.POST.get('description'), request.POST.get('created_teacher_id'), request.POST.get('runtime_limit'), request.POST.get('memory_limit')))
        # insert new problem and cases to database
        try:
            # find teacher from Teacher table
            teacher = Teacher.objects.get(teacher_number=created_teacher_id)
            # add problem to  problem table
            problem = Problem.objects.create(problem_name=problem_name,description=description,teacher=teacher,runtime_limit=runtime_limit,memory_limit=memory_limit)
            response_object['problem_id'] = problem.id

            # add problem_tags
            for problem_tag in problem_tags:
                tag = Tag.objects.get(name=problem_tag)
                problem.tags.add(tag)  # add tag to problem

            # add cases to case table 
            for case in cases:
                case_input = case["input"]
                case_output = case["output"]
                case_type = case["type"] # zero for test, one for example
                weight = case["weight"]
                case_tags = case["tags"]
                # create case in Case  table
                case = Case.objects.create(input=case_input,output=case_output,type=case_type,problem=problem,weight=weight)
                # add case_tags
                for case_tag in case_tags:
                    tag = Tag.objects.get(name=case_tag)
                    case.tags.add(tag)  # add tag to case

            return self.success(response_object)
        except Exception as exception:
            return self.error(err=exception, msg=str(exception))
    


class EditProblemAPI(APIView):
    # response to post request
    def post(self,request):
        response_object = dict()
        # get information from frontend
        try:
            problem_id = int(request.POST.get('problem_id'))
            problem_name = request.POST.get('problem_name')
            description = request.POST.get('description')
            created_teacher_id = request.POST.get('created_teacher_id')
            runtime_limit = request.POST.get('runtime_limit')
            memory_limit = request.POST.get('memory_limit')
            problem_tags = request.POST.get('tags')
            cases = request.POST.get('cases')
        except Exception as exception:
             return self.error(err=exception.args, msg="problem_id:%s, problem_name:%s, description:%s, created_teacher_id:%s,runtime_limit:%s,memory_limit:%s\n"%(request.POST.get('problem_id'),request.POST.get('problem_name'), request.POST.get('description'), request.POST.get('created_teacher_id'), request.POST.get('runtime_limit'), request.POST.get('memory_limit')))
        #  update the problem information
        try:
            # find the teacher
            teacher = Teacher.objects.get(teacher_number=created_teacher_id)
            # obtain the problem by id
            problem = Problem.objects.get(id=int(problem_id))
            # update the problem
            problem.update(problem_name=problem_name,description=description,teacher=teacher,runtime_limit=runtime_limit,memory_limit=memory_limit)
            response_object['problem_id'] = problem.id

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
                old_case.tags.clear()
                old_case.delete()
            # add new cases
            for case in cases:
                case_input = case["input"]
                case_output = case["output"]
                case_type = case["type"] # zero for test, one for example
                weight = case["weight"]
                case_tags = case["tags"]
                # create case in Case  table
                case = Case.objects.create(input=case_input,output=case_output,type=case_type,problem=problem,weight=weight)
                # add case_tags
                for case_tag in case_tags:
                    tag = Tag.objects.get(name=case_tag)
                    case.tags.add(tag) 

            return self.success(response_object)
        except Exception as exception:
            return self.error(err=exception, msg=str(exception))
    


class DeleteProblemAPI(APIView):
    def post(self, request):
        try:
            problem_id = int(request.POST.get('problem_id'))
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