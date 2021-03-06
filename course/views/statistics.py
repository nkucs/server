from utils.api import APIView
from course.models import Course,CourseTeacher
from lab.models import Lab, LabProblem
from user.models import Teacher, User
from lecture.models import Lecture, LectureProblem
from utils.api import APIView, JSONResponse

from django.http import HttpResponse, JsonResponse
from rest_framework import status

class GetProblemDataAPI(APIView):

    def get(self, request):
        """课程题目总数"""
        problem_data = dict()
        try:
            courses_num = Course.objects.all().count()
            courses = Course.objects.all()
            for i in range(courses_num):
                problem_data[courses[i].name] = 0
                lab_num = Lab.objects.filter(course=courses[i].id).count()
                labs = Lab.objects.filter(course=courses[i].id)
                for j in range(lab_num):
                    problem_data[courses[i].name] += LabProblem.objects.filter(lab=labs[j].id).count()
                lecture_num = Lecture.objects.filter(course=courses[i].id).count()
                lectures = Lecture.objects.filter(course=courses[i].id)
                for j in range(lecture_num):
                    problem_data[courses[i].name] += LectureProblem.objects.filter(lecture=lectures[j].id).count()
            return self.success(problem_data)
        except Exception as exception:
            return self.error(err=exception.args)


class GetTeacherCoursesAPI(APIView):
    
    def get(self,request):
        "单个老师课程"
        req=request.GET.get('teacherId','')
        teacher_id=int(req)
        try:
            courses = CourseTeacher.objects.filter(teacher=teacher_id)
            courses_info = []
            print(len(courses))
            for one_course in courses:             
                one_info ={
                    "name":one_course.course.name,
                    "opne_time":one_course.course.start_time,
                    # 'student_number':len(one_course.course.student),
                    'description':one_course.course.description,
                    'course_code':one_course.course.code,
                    'course_id':one_course.course.id
                }
                courses_info.append(one_info)
            return self.success(courses_info)
        except Exception as exception:
            print("error")
            return self.error(err=exception.args)


class GetCourseStudentNumberAPI(APIView):

    def post(self, request):
        """选课学生人数统计"""
        course_ids = request.data['course_ids']
        courses = Course.objects.filter(id__in=course_ids)
        if courses.count() < 1:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        send = {}
        send['ans'] = []
        for id in course_ids:
            if courses.filter(id=id).count() < 1:
                continue
            course = courses.filter(id=id).first()
            temp = {}
            temp['课程'] = course.name
            temp['选课人数'] = course.students.count()
            send['ans'].append(temp)
        return JsonResponse(send, status=status.HTTP_200_OK, safe=False)
