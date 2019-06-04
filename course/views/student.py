from utils.api import APIView
from course.models import Course, Message
from course.serializers import CourseSerializers
from utils.api import JSONResponse
from django.forms import model_to_dict


class GetAllCourseAPI(APIView):
    #OK#
    def get(self, request):
        AllCourse = Course.objects.all()
        AllCourseResult = []
        for item in AllCourse:
            item_result = model_to_dict(item)
            del item_result['students']
            del item_result['teachers']
            AllCourseResult.append(item_result)
        return self.success(AllCourseResult)


class GetAllMessageAPI(APIView):
    #OK#
    def get(self, request):
        AllMessage = Message.objects.all()
        AllMessageResult = []
        for item in AllMessage:
            item_result = model_to_dict(item)
            AllMessageResult.append(item_result)
        return self.success(AllMessageResult)


class GetMessageOfCourseAPI(APIView):
    #OK#
    def get(self, request):
        course_id = int(request.GET.get('course_id'))
        AllMessage = Message.objects.filter(course=course_id)
        AllMessageResult = []
        for item in AllMessage:
            item_result = model_to_dict(item)
            AllMessageResult.append(item_result)
        return self.success(AllMessageResult)


class GetMyCourseAPI(APIView):
    # 根据student_number找到他的所有课程
    def get(self, request):
        studentNumber = request.GET.get('studentNumber')
        AllCourse = Course.objects.all()
        MyCourses = []
        for item in AllCourse:
            item_result = model_to_dict(item)
            for student in item_result['students']:
                print(student.student_number)
                stu_num=""+student.student_number
                if stu_num == studentNumber:
                    del item_result['students']
                    del item_result['teachers']
                    MyCourses.append(item_result)
                    break

        return self.success(MyCourses)

class GetMyCourseByIDAPI(APIView):
    # 根据student的user id找到他的所有课程
    def get(self, request):
        studentID = request.GET.get('studentID')
        AllCourse = Course.objects.all()
        MyCourses = []
        for item in AllCourse:
            item_result = model_to_dict(item)
            for student in item_result['students']:
                stu_id=str(student.user.id)
                if stu_id == studentID:
                    del item_result['students']
                    del item_result['teachers']
                    MyCourses.append(item_result)
                    break

        return self.success(MyCourses)