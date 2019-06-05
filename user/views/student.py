from utils.api import APIView, JSONResponse
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from course.models import Course
import math
from django.contrib.auth.models import Group
from django.db.models import Model
from utils.api import APIView, JSONResponse
from ..models import Student,UserStatus,Gender,User
from django.forms import model_to_dict

class GetStudentAPI(APIView):
    def get(self, request):
        # get information from frontend #OK#
        id_user = int(request.GET.get('id_user'))
        NowStudent = Student.objects.get(user=id_user)
        NowStudentResult = model_to_dict(NowStudent)
        del NowStudentResult['followers']
        del NowStudentResult['achievements']
        return self.success(NowStudentResult)

def LoginStudentAPI(APIView):
    # Login API
    def post(self, request):
        studentName = request.GET.get('name')
        studentPasswordHash = request.GET.get('password_hash')
        studentUser = Student.objects.get(name=studentName)
        if studentUser:
            if studentUser.password_hash == studentPasswordHash:
                return HttpResponse(status=0)
            else:
                return HttpResponse(status=1)
        else:
            return HttpResponse(status=-1)


def GetStudentCourseAPI(APIView):
    # Get Course of an Student
    def get(self, request):
        idStudent = int(request.GET.get('id_student'))
        courseListID = CourseStudent.object.filter(id_student = idStudent)
        courseList = []
        for item in courseListID.data:
            studentCourse = Course.object.get(id = item.id_course)
            courseList.append(studentCourse)
        courseListSerializer = CourseSerializers(courseList)
        return JsonResponse(courseListSerializer.data,status=status.HTTP_200_OK)

def GetMessageAPI(APiView):
    pass




class GetStudentListAPI(APIView):
    response_class = JSONResponse

    def post(self, request):
        response_object = dict()
        # get information from frontend
        try:
            items = int(request.data.get('items_per_page'))
            page = int(request.data.get('page'))
            searchDict = request.data.get("search_items")
            student_number = searchDict['id']
            user_name = searchDict["nick_name"]
            user_username = searchDict["account"]
            user_status = searchDict["state"]
            gender = searchDict["gender"]
        except Exception as exception:
            return self.error(err=[400])
        try:
            #if
            
            if user_status !="":
                student_sta = UserStatus.objects.get(name=user_status)
                user_status = student_sta.name
            students = Student.objects.filter(
                student_number__contains=student_number 
            )
            ans = []
            if gender !="":
                student_gen = Gender.objects.get(name=gender)
                gender = student_gen.name
                for student in students:
                    if gender == student.user.gender.name:
                        if  user_status in student.user.user_status.name:
                            if user_name in student.user.name:
                                if user_username in student.user.username:
                                    ansDict = dict()
                                    ansDict['id'] = student.student_number
                                    ansDict['name'] = student.user.name
                                    ansDict['gender'] = student.user.gender.name
                                    ansDict['account'] = student.user.username
                                    ansDict['user_status'] = student.user.user_status.name
                                    ans.append(ansDict)
            else:
                for student in students:
                    if  user_status in student.user.user_status.name:
                        if user_name in student.user.name:
                            if user_username in student.user.username:
                                ansDict = dict()
                                ansDict['id'] = student.student_number
                                ansDict['name'] = student.user.name
                                ansDict['gender'] = student.user.gender.name
                                ansDict['account'] = student.user.username
                                ansDict['user_status'] = student.user.user_status.name
                                ans.append(ansDict)
                                
            if (ans.__len__() <= items * (page - 1)):
                ans = []
            else:
                start = items * (page - 1)
                ans = ans[start:start + items]
            pages = math.ceil(ans.__len__() / items)
            response_object['current_page'] = page
            response_object['total_pages'] = pages
            response_object['students'] = ans
            return self.success(response_object)
        except Exception as exception:
            return self.error(err=exception.args)


class DeleteStudentAPI(APIView):
    response_class = JSONResponse
    #根据student_number删除
    def post(self, request):
        response_object = dict()
        try:
            id = request.data.get('id')
        except Exception as exception:
            msg = "id:%s\n" % (request.data.get('id'))
            return self.error(err=[400, msg])
        try:
            student_number = Student.objects.get(student_number=id)
            id_new = student_number.user
            id_new.delete()
            student_number.delete()
            response_object["state_code"] = 0
            return self.success(response_object)
        except Exception as exception:
            response_object["state_code"] = -1
            return self.error(err=exception.args, msg=response_object)


