from django.db import models
from course.models import Course, CourseResource
from problem.models import Problem
from submission.models import ProblemSubmission
from user.models import Student


class Lab(models.Model):
    """实验课"""

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    attachment_weight = models.IntegerField()
    problem_weight = models.IntegerField()
    report_required = models.BooleanField()
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    resources = models.ManyToManyField(CourseResource, blank=True, related_name='labs')
    problems = models.ManyToManyField(Problem, blank=True, related_name='labs', through='LabProblem')


class LabProblem(models.Model):
    """实验课编程题联系表"""

    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    weight = models.IntegerField()
    language = models.IntegerField()


class LabSubmission(models.Model):
    """实验课提交记录"""

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    submission_time = models.DateTimeField(auto_now=True)
    attachment_grade = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    problem_grade = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    problem_submissions = models.ManyToManyField(ProblemSubmission, blank=True, related_name='lab_submissions',
                                                 through='LabSubmissionProblemSubmission')


class Attachment(models.Model):
    """学生提交的附件"""

    lab_submission = models.ForeignKey(LabSubmission, null=True, on_delete=models.SET_NULL)
    file = models.FileField(upload_to='uploads/attachments/%Y/%m/')


class LabSubmissionProblemSubmission(models.Model):
    """实验课提交与编程题提交联系表"""

    lab_submission = models.ForeignKey(LabSubmission, on_delete=models.CASCADE)
    problem_submission = models.ForeignKey(ProblemSubmission, on_delete=models.CASCADE)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
