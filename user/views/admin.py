import math
from django.contrib.auth.models import Group
from django.db.models import Model

from utils.api import APIView, JSONResponse
from ..serializers import RoleSerializers, TeacherSerializer
from ..models import Role, Permission, User


class GetRoleAPI(APIView):
    response_class = JSONResponse

    # get方法，参数用params放在url后面

    def get(self, request):
        # get information from frontend
        try:
            id = int(request.GET.get('id_role'))
        except Exception as exception:
            msg = "id_role:%s\n" % (request.GET.get('id_role'))
            return self.error(err=[400, msg])
        try:
            role = Role.objects.get(group_id=id)
            ansDict = RoleSerializers(role).data
            ansDict['name'] = role.group.name
            return self.success(ansDict)
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
            if (name is None or description is None or permission is None):
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
            if (searchDict['role_id'] != ""):
                id = int(searchDict['role_id'])
            name = searchDict["role_name"]
            description = searchDict["role_description"]
        except Exception as exception:
            return self.error(err=[400])
        try:
            if (searchDict['role_id'] != ""):
                roles = Role.objects.filter(
                    description__contains=description,
                    group_id=id)
            else:
                roles = Role.objects.filter(description__contains=description)
            ans = []
            for role in roles:
                if (name in role.group.name):
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
            if (roleList.__len__() <= items * (page - 1)):
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
            if (name is None or description is None or permission is None):
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


class Paginator:

    def __init__(self, obj_set, serializer, page, page_size):
        self.__obj_set = obj_set
        self.__serializer = serializer
        self.__page = page
        self.__page_size = page_size

    def get_response(self):
        objects_count = self.__obj_set.count()
        pages_count = math.ceil(objects_count / self.__page_size)

        if self.__page > pages_count:
            self.__page = pages_count
        if self.__page < 1:
            self.__page = 1
        offset = (self.__page - 1) * self.__page_size
        objs = self.__obj_set.all()[
                offset:offset + self.__page_size if offset + self.__page_size <= objects_count else objects_count]

        response = {
            'page': self.__page,
            'count': objects_count,
            'total_pages': pages_count,
            'contents': []
        }
        for obj in objs:
            response['contents'].append(self.__serializer(obj).data)

        return response


class GetRoleTeacherListAPI(APIView):

    def get(self, request):
        role_id = int(request.GET.get('id', 0))
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))

        try:
            group = Group.objects.get(id=role_id)
        except Group.DoesNotExist:
            return self.error(err=404, msg='Role does not exist.')

        paginator = Paginator(group.user_set, TeacherSerializer, page, page_size)
        return self.success(data=paginator.get_response())


class GetRoleAddTeacherListAPI(APIView):
    pass


class RoleTeacherAPI(APIView):
    pass
