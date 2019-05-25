import math
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


class DeleteRoleAPI(APIView):
    response_class = JSONResponse

    def post(self, request):
        response_object = dict()
        try:
            id = int(request.data.get('id'))
        except Exception as exception:
            msg = "id:%s\n" % (request.data.get('id'))
            return self.error(err=[400, msg])
        try:
            role = Role.objects.get(group_id=id)
            group = Group.objects.get(id=role.group_id)
            group.delete()
            role.delete()
            response_object["state_code"] = 0
            return self.success(response_object)
        except Exception as exception:
            response_object["state_code"] = -1
            return self.error(err=exception.args, msg=response_object)


class CreateRoleAPI(APIView):
    response_class = JSONResponse

    def post(self, request):
        response_object = dict()
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
            response_object["state_code"] = 0
            return self.success(response_object)
        except Exception as exception:
            response_object["state_code"] = -1
            return self.error(err=exception.args, msg=response_object)


class GetRoleListAPI(APIView):
    response_class = JSONResponse

    def post(self, request):
        response_object = dict()
        # get information from frontend
        try:
            items = int(request.data.get('items_per_page'))
            page = int(request.data.get('page'))
            searchDict = request.data.get("search_request")
            if(searchDict['role_id'] != ""):
                id = int(searchDict['role_id'])
            name = searchDict["role_name"]
            description = searchDict["role_description"]
        except Exception as exception:
            return self.error(err=[400])
        try:
            if(searchDict['role_id'] != ""):
                roles = Role.objects.filter(
                    description__contains=description,
                    group_id=id)
            else:
                roles = Role.objects.filter(description__contains=description)
            ans = []
            for role in roles:
                if(name in role.group.name):
                    ans.append(role)
            roleList = []
            pages = math.ceil(ans.__len__() / items)
            for item in ans:
                roleDict = dict()
                roleDict['id_role'] = item.group.id
                roleDict['name'] = item.group.name
                roleDict['description'] = item.description
                roleDict['role_number'] = item.group.user_set.count()
                roleList.append(roleDict)
            if(roleList.__len__() <= items * (page - 1)):
                roleList = []
            else:
                start = items * (page - 1)
                roleList = roleList[start:start + items]
            response_object['current_page'] = page
            response_object['total_pages'] = pages
            response_object['roles'] = roleList
            return self.success(response_object)
        except Exception as exception:
            return self.error(err=exception.args)


class ModifyRoleAPI(APIView):
    response_class = JSONResponse

    def post(self, request):
        response_object = dict()
        try:
            id = request.data.get('id_role')
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
            # update role
            Group.objects.filter(id=id).update(name=name)
            Role.objects.filter(group_id=id).update(
                description=description)
            role = Role.objects.get(group_id=id)
            role.permission.clear()
            for per in permission:
                role.permission.add(Permission.objects.get(id=per))
            response_object["state_code"] = 0
            return self.success(response_object)
        except Exception as exception:
            response_object["state_code"] = -1
            return self.error(err=exception.args, msg=response_object)
