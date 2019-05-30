from django.contrib import admin
from user.models import User, Student, Teacher, Admin
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Admin)
