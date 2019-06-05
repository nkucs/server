from utils.api import APIView
from ..models import Student
import datetime


class GetStudentStatAPI(APIView):

    def get(self, request):

        new_year = datetime.datetime.now().year % 100
        new_month = datetime.datetime.now().month
        if new_month > 8:
            new_year += 1
        stu_num = dict()
        try:
            for i in range(5):
                stu_num["20" + str(new_year-5+i)] = \
                    Student.objects.filter(student_number__startswith=str(new_year-5+i)).count()
        except Student.DoesNotExist:
            return self.error("error")
        return self.success(stu_num)
        