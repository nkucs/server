from utils.api import APIView, JSONResponse
from ..models import Role
from ..serializers import RoleSerializers


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
