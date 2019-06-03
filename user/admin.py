from .models import User, UserStatus, Permission, Gender, Role, Student, Teacher, Admin, RankHistory, Achievement, \
    StudentAchievement, AnnualReport
from django.contrib import admin


admin.site.register(User)
admin.site.register(UserStatus)
admin.site.register(Permission)
admin.site.register(Gender)
admin.site.register(Role)
admin.site.register(RankHistory)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Admin)
admin.site.register(Achievement)
admin.site.register(StudentAchievement)
admin.site.register(AnnualReport)



