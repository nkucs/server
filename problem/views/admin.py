from ..models import Problem
from utils.api import APIView, JSONResponse, FILEResponse
from ..serializers import GetProblemsSerializer


from ..models import Lab

class GetProblemsAPI(APIView):
    response_class = JSONResponse
    def get(self, request):
        # suppose that one page contains 10 lab information
        list_count = 10
        # initialize the response object
        response_object = dict()
        # get information from frontend
        try:
            current_page = int(request.GET.get('page'))
            program_name = request.GET.get('program_name')
            page_length = int(request.GET.get('page_length'))
            created_teacher_name = request.GET.get('created_teacher_name')
            course_name = request.GET.get('course_name')
        except Exception as exception:
            return self.error(err=exception.args, msg="program name:%s, page:%s\n"%(request.GET.get('program_name'), request.GET.get('page')))
        
        try:
            # query from database
            problem_list = Problem.objects.all()[(current_page - 1) * list_count : current_page * list_count].values(
                'id', 'name', 'id_teacher', 'created_at', 'submit_count', 'accepted_count')
            
            # update response object
            response_object['total_pages'] = page_length
            response_object['current_page'] = current_page
            response_object['problems'] = GetProblemsSerializer(problem_list, many=True).data

            return self.success(response_object)
        except Exception as exception:
            return self.error(err=exception.args, msg=str(exception))