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
            for one_course in courses:
                one_course_info = Course.objects.get(id=one_course.course)
                one_info ={
                    "name":one_course_info.name,
                    "opne_time":one_course_info.start_time,
                    'student_number':len(one_course_info.student),
                    'description':one_course_info.description
                }
                course_info.append(one_info)
            return self.success(course_info)
        except Exception as exception:
            return self.error(err=exception.args)


class GetCourseStudentNumberAPI(APIView):

    def get(self, request):
        """选课学生人数统计"""
        cur_ids = request.GET['course_id']  # is a list
        cid_len = len(cur_ids)
        if cid_len < 1:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        courses, cur_names, cur_stds, cstd_nums = [], [], [], []
        for i in range(0, cid_len):
            get_courses = Course.objects.filter(id=cur_ids[i])
            if get_courses.count() < 1:
                return HttpResponse(status=status.HTTP_404_NOT_FOUND)
            courses.append(get_courses.first())
            cur_names.append(courses[i].name)
            cur_stds.append(courses[i].students.all())
            cstd_nums.append(cur_stds.count)
        sned = {}
        send['ans'] = []
        for i in range(0, cid_len):
            temp = {}
            temp["课程"] = cur_names[i]
            temp["选课人数"] = cstd_nums[i]
            send['ans'].append(temp)
        return JsonResponse(send, status=status.HTTP_200_OK)