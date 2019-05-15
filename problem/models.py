from django.db import models
from user.models import Teacher


class Language:
    # TODO: 添加语言代码定义，例如
    # TODO: CPP = 1
    # TODO: JAVA = 2
    pass


class Tag(models.Model):
    """题目标签和测试案例标签"""

    name = models.CharField(max_length=128)
    type = models.BooleanField()


class Problem(models.Model):
    """编程题目"""

    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=128)
    description = models.TextField()
    runtime_limit = models.BigIntegerField()
    memory_limit = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    teacher = models.ForeignKey(Teacher, null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag, blank=True, related_name='problems')


class Case(models.Model):
    """测试案例/示例"""

    input = models.TextField(blank=True)
    output = models.TextField(blank=True)
    type = models.BooleanField()
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    weight = models.IntegerField(null=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='cases')
