import math
from django.contrib.auth.models import Group
from utils.api import APIView, JSONResponse
from ..serializers import TeacherSerializers, UserSerializers, AdminSerializers
from ..models import Role, Permission, User, Student, Teacher, Admin, Gender, UserStatus


def getRole(userId):
    user = User.objects.get(id=userId)
    groups = Group.objects.filter(user=user)
    groupNames = []
    for group in groups:
        groupNames.append(group.name)
    if len(groupNames) == 1:
        return groupNames[0]
    else:
        name_string = ','.join(groupNames)
        return name_string



class GetStaffListAPI(APIView):
    """
    获取staff列表信息
    """
    def get(self, request):
        try:
            stafflist = []
            admins = Admin.objects.all()
            for admin in admins:
                adminDict = dict()
                adminDict['key'] = admin.user.id
                adminDict['number'] = admin.admin_number
                adminDict['account'] = admin.user.username
                adminDict['nickname'] = admin.user.name
                adminDict['status'] = admin.user.user_status.name
                adminDict['gender'] = admin.user.gender.name
                adminDict['role'] = getRole(admin.user.id)
                stafflist.append(adminDict)
            teachers = Teacher.objects.all()
            for teacher in teachers:
                teacherDict = dict()
                teacherDict['key'] = teacher.user.id
                teacherDict['number'] = teacher.teacher_number
                teacherDict['account'] = teacher.user.username
                teacherDict['nickname'] = teacher.user.name
                teacherDict['status'] = teacher.user.user_status.name
                teacherDict['gender'] = teacher.user.gender.name
                teacherDict['role'] = getRole(teacher.user.id)
                stafflist.append(teacherDict)
            stafflist.sort(key=lambda e: e.__getitem__('key'))
            return self.success(stafflist)
        except Exception as exception:
            return self.error(err=exception.args)


class GetStaffAPI(APIView):
    """
    获取某staff信息
    """
    def get(self, request):
        try:
            id = request.GET.get('id')
            role = request.GET.get('role')
            staff_id = request.GET.get('staff')
            role = role.split(',')
            role = role[0]
            if role.startswith('admin'):
                admin = Admin.objects.get(admin_number=staff_id)
                adminDict = dict()
                adminDict['id'] = admin.user.id
                adminDict['number'] = admin.admin_number
                adminDict['account'] = admin.user.username
                adminDict['nickname'] = admin.user.name
                adminDict['status'] = admin.user.user_status.name
                adminDict['gender'] = admin.user.gender.name
                adminDict['role'] = getRole(admin.user.id)
                return self.success(adminDict)             
            else: 
                teacher = Teacher.objects.get(teacher_number=staff_id)
                teacherDict = dict()
                teacherDict['id'] = teacher.user.id
                teacherDict['number'] = teacher.teacher_number
                teacherDict['account'] = teacher.user.username
                teacherDict['nickname'] = teacher.user.name
                teacherDict['status'] = teacher.user.user_status.name
                teacherDict['gender'] = teacher.user.gender.name
                teacherDict['role'] = getRole(teacher.user.id)
                return self.success(teacherDict)  
        except Exception as exception:
            return self.error(err=exception.args)






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
            role = role.split(',')
            role = role[0]
            if role.startswith('admin'):
                admin = Admin.objects.get(admin_number=staff_id)
                userId = admin.user.id
                print(userId)
                user = User.objects.get(id=userId)
                user.user_status_id = 3
                user.save()
                admin.delete()               
            else: 
                teacher = Teacher.objects.get(teacher_number=staff_id)
                userId = teacher.user.id
                print(userId)
                user = User.objects.get(id=userId)
                user.user_status_id = 3
                user.save()
                teacher.delete()
            response_object["state_code"] = 0
            return self.success(response_object)
        except Exception as exception:
            response_object["state_code"] = -1
            return self.error(err=exception.args, msg=response_object)


class ResetPwdAPI(APIView):
    """
    重置密码
    """
    def post(self, request):
        response_object = dict()
        try:
            userId = request.data.get('id')
        except Exception as exception:
            msg = "id:%s\n" % (request.data.get('id'))
            return self.error(err=[400, msg])
        try:
            user = User.objects.get(id=userId)
            user.password = '0000'
            user.save()
            response_object["state_code"] = 0
            return self.success(response_object)
        except Exception as exception:
            response_object["state_code"] = -1
            return self.error(err=exception.args, msg=response_object)



class GetOneStaffAPI(APIView):
    response_class = JSONResponse

    # get方法，参数用params放在url后面

    def get(self, request):
        # get information from frontend
        try:
            teacher_number = request.GET.get('teacher_number')
        except Exception as exception:
            msg = "id_role:%s\n" % (request.GET.get('teacher_number'))
            return self.error(err=[400, msg])
        try:
            teacher = Teacher.objects.get(teacher_number=teacher_number)
            ansDict = dict()
            ansDict['teacher_number']=teacher_number
            ansDict['name'] = teacher.user.username
            ansDict['username'] = teacher.user.name
            ansDict['gender'] =teacher.user.gender.name
            ansDict['role']="teacher"
            ansDict['status'] = teacher.user.user_status.name
            return self.success(ansDict)
        except Exception as exception:
            return self.error(err=exception.args)

class CreateStaffAPI(APIView):
    """新建职工"""
    response_class = JSONResponse

    def post(self, request):
        response_object = dict()
        
        try:
           
            name = request.data.get('name')
            username = request.data.get('account')
            teacher_number = request.data.get('teacher_number')
            gender = request.data.get('gender')
            role=request.data.get('role')
            status = request.data.get('status')   
         
            if role is None or name is None or username is None or teacher_number is None or status is None or gender is None:
                raise Exception()
        except Exception as exception:
            msg = "name:%s, teacher_number:%s \n" % (
                request.data.get('name'),
                request.data.get('teacher_number'))
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
            Teacher.objects.create(teacher_number=teacher_number,user_id=user.id)
            response_object["state_code"] = 0
            return self.success(response_object)
        except Exception as exception:
            response_object["state_code"] = -1
            return self.error(err=exception.args, msg=response_object)

class UpdateStaffAPI(APIView):
    """修改教师信息"""
    response_class = JSONResponse

    def post(self, request):
        response_object = dict()
        try:
            name = request.data.get('name')
            username = request.data.get('account')
            teacher_number = request.data.get('teacher_number')
            gender = request.data.get('gender')
            role=request.data.get('role')
            status = request.data.get('status')           
            if role is None or name is None or username is None or teacher_number is None or status is None or gender is None:
                raise Exception()
        except Exception as exception:
            msg = "name:%s, teacher_number:%s \n" % (
                request.data.get('name'),
                request.data.get('teacher_number'))
            return self.error(err=[400, msg])

        try:
            # insert new role into database
            teacher = Teacher.objects.get(teacher_number=teacher_number)
            if Gender.objects.filter(name=gender).count() is 0:
                Gender.objects.create(name=gender)
            if UserStatus.objects.filter(name=status).count() is 0:
                UserStatus.objects.create(name=status)                
            new_status = UserStatus.objects.get(name=status)
            new_gender = Gender.objects.get(name=gender)
            user_id = teacher.user.id
            User.objects.filter(id=user_id).update(name=name,username=username,gender=new_gender,user_status=new_status)
            Teacher.objects.filter(teacher_number=teacher_number).update()
            response_object["state_code"] = 0
            return self.success(response_object)
        except Exception as exception:
            response_object["state_code"] = -1
            return self.error(err=exception.args, msg=response_object)
