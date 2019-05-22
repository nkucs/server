from django.db import models

from lecture.models import Lecture
from problem.models import Problem, Case
from user.models import Student


class ProblemSubmission(models.Model):
    """编程题提交记录"""

    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    program = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now=True)
    runtime = models.BigIntegerField()
    memory = models.BigIntegerField()
    IP = models.CharField(max_length=20)
    language = models.IntegerField()
    cases = models.ManyToManyField(Case, blank=True, related_name='problem_submissions',
                                   through='ProblemSubmissionCase')
    lectures = models.ManyToManyField(Lecture, blank=True, related_name='problem_submissions')

class CaseStatus(models.Model):
    """测试案例通过情况"""

    name = models.CharField(max_length=20)

    @staticmethod
    def default():
        return 1


class ProblemSubmissionCase(models.Model):
    """测试案例与提交联系表"""

    problem_submission = models.ForeignKey(ProblemSubmission, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    case_status = models.ForeignKey(CaseStatus, default=CaseStatus.default, on_delete=models.SET_DEFAULT)
    output_info = models.TextField(blank=True)
