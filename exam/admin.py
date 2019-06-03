from .models import Exam, ExamProblem, StudentExam
from django.contrib import admin


admin.site.register(Exam)
admin.site.register(ExamProblem)
admin.site.register(StudentExam)