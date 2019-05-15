from django.db import models
from oj import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserStatus(models.Model):
    """用户状态"""

    name = models.CharField(max_length=20, unique=True)

    @staticmethod
    def default():
        return 1


class Gender(models.Model):
    """性别"""

    name = models.CharField(max_length=20, unique=True)

    @staticmethod
    def default():
        return 1


class User(AbstractUser):
    """自定义用户基类"""

    name = models.CharField(max_length=20)
    user_status = models.ForeignKey(UserStatus, default=UserStatus.default, on_delete=models.SET_DEFAULT)
    email = models.EmailField(null=True, blank=True)
    gender = models.ForeignKey(Gender, default=Gender.default, on_delete=models.SET_DEFAULT)

    USERNAME_FIELD = 'id'


class Student(models.Model):
    """学生"""

    student_number = models.CharField(max_length=20, unique=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rank_score = models.IntegerField(default=0)
    room = models.CharField(max_length=20, null=True, blank=True)
    province = models.IntegerField(null=True)
    class_name = models.CharField(max_length=20, null=True, blank=True)
    followers = models.ManyToManyField('self', blank=True, related_name='following')
    achievements = models.ManyToManyField('Achievement', blank=True, related_name='students',
                                          through='StudentAchievement')


class Teacher(models.Model):
    """教师"""

    teacher_number = models.CharField(max_length=20, unique=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Admin(models.Model):
    """管理员"""

    admin_number = models.CharField(max_length=20, unique=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class RankHistory(models.Model):
    """排名历史"""

    date = models.DateField(auto_now=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    rank_number = models.IntegerField(default=0)


class Achievement(models.Model):
    """成就"""

    name = models.CharField(max_length=128)
    icon = models.ImageField(upload_to='uploads/achievements/')


class StudentAchievement(models.Model):
    """学生成就联系表"""

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    achieved_at = models.DateTimeField(auto_now=True)


class AnnualReport(models.Model):
    """年度报告"""

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    year = models.IntegerField()
    image = models.ImageField(upload_to='uploads/annual_reports/%Y/')
