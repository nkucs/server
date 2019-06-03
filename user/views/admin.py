import math
from importlib import import_module
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from utils.api import APIView, JSONResponse
from ..serializers import RoleSerializers, TeacherSerializer
from ..models import Role, Permission, User, Student, Teacher, Admin, Gender, UserStatus
from django.db.models import Model


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
                request.data.get('description'))
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
                request.data.get('description'))
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

class UserLoginAPI(APIView):
    """用户登录"""
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    response_class = HttpResponse

    @csrf_exempt
    def post(self, request, usertype):
        response_object = dict()
        data = request.data        
        validType = ['stud', 'admi', 'teac']
        username = data["username"]
        password = data["password"]
        remember = data["rememberMe"]
        if usertype not in validType:
            msg = "Illegal login request."
            return self.error(err=msg)

        user = authenticate(username=username, password=password)
        if not user:
            msg = "Wrong username or password"
            return self.error(err=msg)

        if usertype == 'stud':
            specuser = Student.objects.filter(user=user)
        elif usertype == 'teac':
            specuser = Teacher.objects.filter(user=user)
        else:
            specuser = Admin.objects.filter(user=user)
        if not specuser.exists():
            msg = "Permission denied."
            return self.error(err=msg)

        auth.login(request, user)
        if not remember:
            request.session.set_expiry(0)
        else:
            request.session.set_expiry(60 * 60 * 24 * 30)
        response_object["user_id"] = user.id
        return self.success(response_object)

class UserLogoutAPI(APIView):
    """用户退出登录"""
    def get(self, request):
        response_object = dict()
        auth.logout(request)
        response_object["state_code"] = 0
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


class CreateStudentAPI(APIView):
    """新建学生"""
    response_class = JSONResponse

    def post(self, request):
        response_object = dict()
        try:
            name = request.data.get('name')
            username = request.data.get('account')
            student_number = request.data.get('student_number')
            gender = request.data.get('gender')
            room = request.data.get('room')
            province = int(request.data.get('province'))
            status = request.data.get('status')
            class_name = request.data.get('class_name')
            if name is None or username is None or student_number is None or room is None or province is None or status is None or class_name is None or gender is None:
                raise Exception()
        except Exception as exception:
            msg = "name:%s, description:%s \n" % (
                request.data.get('name'),
                request.data.get('account'))
            return self.error(err=[400, msg])

        try:
            # insert new role into database
            if UserStatus.objects.filter(name=status).count() is 0:
                UserStatus.objects.create(name=status)
            status_ = UserStatus.objects.get(name=status)       
            if Gender.objects.filter(name=gender).count() is 0:
                Gender.objects.create(name=gender)
            gender_ = Gender.objects.get(name=gender)
            User.objects.create(username=username,name=name,user_status=status_,gender=gender_)
            user = User.objects.get(username=username)
            Student.objects.create(student_number=student_number,user=user,room=room,province=province,class_name=class_name)
            response_object["state_code"] = 0
            return self.success(response_object)
        except Exception as exception:
            response_object["state_code"] = -1
            return self.error(err=exception.args, msg=response_object)


class GetStudentAPI(APIView):
    response_class = JSONResponse

    # get方法，参数用params放在url后面

    def get(self, request):
        # get information from frontend
        try:
            student_number = request.GET.get('student_number')
        except Exception as exception:
            msg = "id_role:%s\n" % (request.GET.get('student_number'))
            return self.error(err=[400, msg])
        try:
            student = Student.objects.get(student_number=student_number)
            ansDict = dict()
            ansDict['name'] = student.user.name
            ansDict['username'] = student.user.username
            ansDict['gender'] = student.user.gender.name
            ansDict['room'] = student.room
            ansDict['province'] = str(student.province)
            ansDict['class_name'] = student.class_name
            ansDict['status'] = student.user.user_status.name
            return self.success(ansDict)
        except Exception as exception:
            return self.error(err=exception.args)


class UpdateStudentAPI(APIView):
    """修改学生信息"""
    response_class = JSONResponse

    def post(self, request):
        response_object = dict()
        try:
            name = request.data.get('name')
            username = request.data.get('account')
            student_number = request.data.get('student_number')
            gender = request.data.get('gender')
            room = request.data.get('room')
            province = int(request.data.get('province'))
            status = request.data.get('status')
            class_name = request.data.get('class_name')
            if name is None or username is None or student_number is None or room is None or province is None or status is None or class_name is None or gender is None:
                raise Exception()
        except Exception as exception:
            msg = "name:%s, description:%s \n" % (
                request.data.get('name'),
                request.data.get('account'))
            return self.error(err=[400, msg])

        try:
            # insert new role into database
            student = Student.objects.get(student_number=student_number)
            if Gender.objects.filter(name=gender).count() is 0:
                Gender.objects.create(name=gender)
            if UserStatus.objects.filter(name=status).count() is 0:
                UserStatus.objects.create(name=status)           
            new_status = UserStatus.objects.get(name=status)
            new_gender = Gender.objects.get(name=gender)
            user_id = student.user.id
            User.objects.filter(id=user_id).update(name=name,username=username,gender=new_gender,user_status=new_status)
            Student.objects.filter(student_number=student_number).update(room=room,province=province,class_name=class_name)
            response_object["state_code"] = 0
            return self.success(response_object)
        except Exception as exception:
            response_object["state_code"] = -1
            return self.error(err=exception.args, msg=response_object)




