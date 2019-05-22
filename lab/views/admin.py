from utils.api import APIView, JSONResponse
from ..serializers import LabSerializers1
from ..models import Lab

class GetLabsAPI(APIView):
    response_class = JSONResponse
    def get(self, request):
        # suppose that one page contains 10 lab information
        list_count = 10
        # initialize the respones object
        response_object = dict()
        # get information from frontend
        try:
            course_id = int(request.GET.get('course_id'))
            page = int(request.GET.get('page'))
        except Exception as exception:
            self.error(msg=exception, err="course_id:%s, page:%s\n"%(request.GET.get('course_id'), request.GET.get('page')))
        
        try:
            # query from database
            labs_number = Lab.objects.filter(course=course_id).count()
            labs_list = Lab.objects.filter(course=course_id)[(page - 1) * list_count : page * list_count].values('id', 'name')
            # update response object
            response_object['total_pages'] = labs_number // list_count + 1
            response_object['current_page'] = page
            response_object['labs'] = LabSerializers1(labs_list, many=True).data

            return self.success(response_object)
        except Exception as exception:
            return self.error(msg=exception, err=type(exception))
            