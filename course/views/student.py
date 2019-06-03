from utils.api import APIView
from course.models import Course
from course.serializers import CourseSerializer
from user.models import Student
from django.http import HttpResponse, JsonResponse

class GetCourseAPI(APIView):
    def get(self, request):
        
        user_id = int(request.GET.get("user_id"))
        # Get the stu object first and then stu.courses.all() to get all the courses. Serilizer converts the package to json and returns it to the front end.
        student = Student.objects.filter(id=user_id)
        courses = student.courses.all()
        #before there is successed
        serializer = CourseSerializer(courses, many=True)
        return JsonResponse(serializer.data)   # [{}{}{}]