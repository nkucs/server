from django.db import models

from course.models import Course
from problem.models import Problem
from submission.models import ProblemSubmission
from user.models import Student


class Exam(models.Model):
    """考试"""

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    start_time = models.DateTimeField()
    duration = models.DurationField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(Student, blank=True, related_name='exams', through='StudentExam')


class ExamProblem(models.Model):
    """考试编程题联系表"""

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    type = models.IntegerField()
    weight = models.IntegerField()
    language = models.IntegerField()


class StudentExam(models.Model):
    """学生考试联系表"""

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    type = models.IntegerField()
    grade = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    password = models.CharField(max_length=20)
    finished = models.BooleanField(default=False)
    problem_submissions = models.ManyToManyField(ProblemSubmission, blank=True, related_name='student_exams')
