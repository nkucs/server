from django.contrib.auth.models import Group
from utils.api import APIView, JSONResponse
from ..serializers import RoleSerializers
from ..models import Role, Permission


class GetRoleAPI(APIView):
    response_class = JSONResponse
    # get方法，参数用params放在url后面

    def get(self, request):
        # get information from frontend
        try:
            id = int(request.data.get('id_role'))
        except Exception as exception:
            msg = "id_role:%s\n" % (request.data.get('id_role'))
            return self.error(err=[400, msg])
        try:
            role = Role.objects.get(group_id=id)
            return self.success(RoleSerializers(role).data)
        except Exception as exception:
            return self.error(err=exception.args)


class CreateRoleAPI(APIView):
    response_class = JSONResponse

    def post(self, request):
        response_object = dict()
        # get information from frontend
        try:
            name = request.data.get('name')
            description = request.data.get('description')
            permission = request.data.get('permission')
            if(name is None or description is None or permission is None):
                raise Exception()
        except Exception as exception:
            msg = "name:%s, description:%s\n" % (
                request.data.get('name'),
                request.data.get('description'),
                request.data.get('permission'))
            return self.error(err=[400, msg])
        try:
            # insert new role into database
            Group.objects.create(name=name)
            group = Group.objects.get(name=name)
            role = Role.objects.create(group=group, description=description)
            for per in permission:
                role.permission.add(Permission.objects.get(id=per))
            return self.success(RoleSerializers(role).data)
        except Exception as exception:
            return self.error(err=exception.args)
