from utils.api import APIView
from course.models import Course
from lab.models import Lab, LabProblem
from lecture.models import Lecture, LectureProblem


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
