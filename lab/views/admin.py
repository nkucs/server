from course.models import CourseResource
from utils.api import APIView, JSONResponse, FILEResponse
from ..serializers import LabSerializers, GetLabSerializer

from ..models import Lab

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
            labs_list = Lab.objects.filter(course=course_id)[(page - 1) * list_count : page * list_count].values('id', 'name')
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
            return self.response(course_resource.file)
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
        lab_id = request.GET.get('lab_id')
        # check if lab_id exists
        if not lab_id:
            #not found
            return self.error(msg=f"lab_id key is None", err=request.GET)
        try:
            # query for the lab
            lab_object = Lab.objects.get(id=lab_id)
            return self.success(GetLabSerializer(lab_object).data)
        except Exception as e:
            # not found
            return self.error(msg=str(e), err=e.args)
