from .models import Course, CourseResource, CourseTeacher, CourseTeacherType, Message
from django.contrib import admin


admin.site.register(Course)
admin.site.register(CourseResource)
admin.site.register(CourseTeacherType)
admin.site.register(CourseTeacher)
admin.site.register(Message)