from django.db import models
from user.models import Student, Teacher


class CourseTeacherType(models.Model):
    """课程教师类型"""

    name = models.CharField(max_length=20, unique=True)

    @staticmethod
    def default():
        return 1


class CourseTeacher(models.Model):
    """教师课程联系表"""

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    course_teacher_type = models.ForeignKey(CourseTeacherType, default=CourseTeacherType.default,
                                            on_delete=models.SET_DEFAULT)


class Course(models.Model):
    """课程"""

    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=128)
    start_time = models.DateField()
    end_time = models.DateField()
    description = models.TextField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(Student, blank=True, related_name='courses')
    teachers = models.ManyToManyField(Teacher, blank=True, related_name='courses', through=CourseTeacher)


class Message(models.Model):
    """消息"""

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now=True)


class CourseResource(models.Model):
    """课程资源"""

    name = models.CharField(max_length=128)
    file = models.FileField(upload_to='uploads/course_resources/%Y/%m/')
    size = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now=True)
    modified_at = models.DateTimeField(auto_now_add=True)
