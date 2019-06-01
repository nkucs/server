import math
from django.contrib.auth.models import Group
from utils.api import APIView, JSONResponse
from ..serializers import TeacherSerializers, UserSerializers, AdminSerializers
from ..models import  Admin, Teacher


class GetStaffListAPI(APIView):
    """
    获取staff信息
    """
    def get(self, request):
        admin = Admin.objects.all()
        admin_serializers = AdminSerializers(admin, many=True)
        teachers = Teacher.objects.all()
        teachers_serializers = TeacherSerializers(teachers, many=True)
        datalist = admin_serializers.data + teachers_serializers.data
        print(datalist)
        return self.success(datalist)


class GetStaffAPI(APIView):
    """
    获取某staff信息
    """
    def get(self, request):
        admin_id = request.GET.get('id')
        admin = Admin.objects.get(id=admin_id)
        admin_serializers = AdminSerializers(admin)
        return self.success(admin_serializers.data)





class DeleteStaffAPI(APIView):
    """
    获取删除指定staff信息
    """
    def post(self, request):
        response_object = dict()
        try:
            id = request.data.get('id')
            role = request.data.get('role')
            staff_id = request.data.get('staff')
                # response_object["state_code"] = role
            if role == 'admin1':
                admin = Admin.objects.get(admin_number=staff_id)
                admin.delete()               
             # teacher = Teacher.objects.get(id=staff_id)
                # teacher.delete()
            else: 
                teacher = Teacher.objects.get(admin_number=staff_id)
                teacher.delete()
            # role.delete()
            response_object["state_code"] = 0
            return self.success(response_object)
        except Exception as exception:
            response_object["state_code"] = -1
            return self.error(err=exception.args, msg=response_object)
