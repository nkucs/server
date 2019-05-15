from django.db import models
from course.models import Course, CourseResource
from problem.models import Problem


class Lecture(models.Model):
    """主讲课"""

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    resources = models.ManyToManyField(CourseResource, blank=True, related_name='lectures')
    problems = models.ManyToManyField(Problem, blank=True, related_name='lectures', through='LectureProblem')


class LectureProblem(models.Model):
    """主讲课编程题联系表"""

    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    language = models.IntegerField()
