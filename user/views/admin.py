import math
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
<<<<<<< HEAD
from django.contrib.sessions.models import Session
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from utils.api import APIView, JSONResponse
from ..serializers import RoleSerializers
from ..models import Role, Permission, User, Student, Teacher, Admin
=======
from django.db.models import Model

from utils.api import APIView, JSONResponse
from ..serializers import RoleSerializers, TeacherSerializer
from ..models import Role, Permission, User
>>>>>>> b63d99b93fb034c73c7929bd17274fd2e1abbf9a


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

class UserAuthAPI(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    # permission_classes = (IsAuthenticated,)
    response_class = HttpResponse

    def post(self, request, usertype):
        validType = ['stud', 'admi', 'teac']
        if usertype in validType:
            response_object = dict()
            data = request.data
            username = data["username"]
            password = data["password"]
            remember = data["rememberMe"]
        else:
            msg = "Illegal login request."
            return self.error(err=msg)
        user = authenticate(username=username, password=password)
        if not user:
            response_object["state_code"] = -1
            msg = "Wrong username or password"
            return self.error(err=msg, msg=response_object)      
        else:
            user_id = user.id
            if usertype == 'stud':
                user = Student.objects.get(user_id=user_id)
            elif usertype == 'teac':
                user = Teacher.objects.get(user_id=user_id)
            else:
                user = Admin.objects.get(user_id=user_id)
            if user is None:
                response_object["state_code"] = -1
                msg = "Permission denied."
                return self.error(err=msg, msg=response_object)
        if not remember:
            request.session.flush()
        else:
            request.session["user_id"] = user.id
            request.session.create()
            sessionID = request.session.session_key
            response_object["sessionID"] = sessionID
            print('sessionID:', sessionID)
        auth.login(request, user)
        response_object["state_code"] = 0
        response_object["user_id"] = user.id
        return self.success(response_object)


class Paginator:
    """分页器"""

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
    """获取某角色下教师列表"""

    def get(self, request):
        role_id = int(request.GET.get('id', 0))
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        name_filter = request.GET.get('name', '')
        user_id_filter = int(request.GET.get('user_id', 0))
        teacher_number_filter = request.GET.get('teacher_number', '')

        try:
            group = Group.objects.get(id=role_id)
        except Group.DoesNotExist:
            return self.error(err=404, msg='Role does not exist.')

        users = group.user_set
        if name_filter != '':
            users = users.filter(name__contains=name_filter)
        if user_id_filter != 0:
            users = users.filter(id=user_id_filter)
        if teacher_number_filter != '':
            users = users.filter(teacher__teacher_number__startswith=teacher_number_filter)

        paginator = Paginator(users, TeacherSerializer, page, page_size)
        return self.success(data=paginator.get_response())


class GetRoleAddTeacherListAPI(APIView):
    """获取某角色可添加的教师列表"""

    def get(self, request):
        role_id = int(request.GET.get('id', 0))
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        name_filter = request.GET.get('name', '')
        user_id_filter = int(request.GET.get('user_id', 0))
        teacher_number_filter = request.GET.get('teacher_number', '')

        try:
            group = Group.objects.get(id=role_id)
        except Model.DoesNotExist:
            return self.error(err=404, msg='Role does not exist.')

        users = User.objects.exclude(groups=group)
        users = users.filter(teacher__isnull=False)
        if name_filter != '':
            users = users.filter(name__contains=name_filter)
        if user_id_filter != 0:
            users = users.filter(id=user_id_filter)
        if teacher_number_filter != '':
            users = users.filter(teacher__teacher_number__startswith=teacher_number_filter)

        paginator = Paginator(users, TeacherSerializer, page, page_size)

        return self.success(data=paginator.get_response())


class RoleTeacherAPI(APIView):
    """分配角色或删除分配"""

    def post(self, request):
        distributions = request.data.get('distribution', [])

        for distribution in distributions:
            user_id = distribution['id_user']
            role_id = distribution['id_role']

            try:
                user = User.objects.get(id=user_id)
                group = Group.objects.get(id=role_id)
            except User.DoesNotExist:
                return self.error(err=404, msg='User ' + str(user_id) + ' does not exist.')
            except Group.DoesNotExist:
                return self.error(err=404, msg='Role ' + str(role_id) + ' does not exist.')

            group.user_set.add(user)

        return self.success({'state_code': 0})

    def delete(self, request):
        remove_list = request.data.get('distribution', [])

        for remove_item in remove_list:
            user_id = remove_item['id_user']
            role_id = remove_item['id_role']

            try:
                user = User.objects.get(id=user_id)
                group = Group.objects.get(id=role_id)
            except User.DoesNotExist:
                return self.error(err=404, msg='User ' + str(user_id) + ' does not exist.')
            except Group.DoesNotExist:
                return self.error(err=404, msg='Role ' + str(role_id) + ' does not exist.')

            group.user_set.remove(user)

        return self.success({'state_code': 0})
