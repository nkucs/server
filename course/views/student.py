from utils.api import APIView
from course.models import Course
from course.serializers import CourseSerializers
from utils.api import JSONResponse
from django.forms import model_to_dict


class GetAllCourseAPI(APIView):
    def get(self, request):
        AllCourse = Course.objects.all()
        AllCourseResult = []
        AllCourseResult.append(model_to_dict(AllCourse[0]))
        AllCourseResult.append(model_to_dict(AllCourse[1]))
        return self.success(AllCourseResult)
        

class GetMyCourseAPI(APIView):
    response_class = JSONResponse

    def post(self, request):
        esponse = dict()
        student_number = request.GET.get('studentNumber')
        page_length = request.GET.get('pageLength')
        page = request.GET.get('page')
        try:
            student = Student.objects.get(student_number=student_number)
            courses_student = Course.students.courses.objects.filter(
                id_student=student.id)
            paginator = Paginator(courses_student, page_length)
            response['totalPages'] = paginator.num_pages
            try:
                courses_student = paginator.page(page)
                response['currentPage'] = page
            except PageNotAnInteger:
                courses_student = paginator.page(1)
                response['currentPage'] = 1
            except EmptyPage:
                courses_student = paginator.page(paginator.num_pages)
                response['currentPage'] = paginator.num_pages
            courses = list()
            for course in courses_student:
                courses.append(course.course)
            courses_info = list()
            for course in courses:
                courses_info.push(course)
            response['courses'] = courses_info
            return self.success(response)
        except Exception as e:
            return self.error(msg=str(e), err=e.args)
