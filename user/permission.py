from django.contrib.auth.models import Group
from .models import User, Permission


def getPermission(index):
    # user = User.objects.create_user(username='用户名',password='密码',email='邮箱')
    user = User.objects.get(id=4)
    groups = Group.objects.filter(user=user)
    permissionNeeded = Permission.objects.get(id=index)
    for group in groups:
        permissions = group.role.permission.all()
        for permission in permissions:
            if permission == permissionNeeded:
                return True
    return False
