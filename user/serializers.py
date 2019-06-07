from rest_framework import serializers
from .models import Role, User
from django.db.utils import IntegrityError


class RoleSerializers(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = '__all__'

from rest_framework import serializers
from .models import Role, Gender, UserStatus, User, Admin, Teacher
from django.db.utils import IntegrityError


class RoleSerializers(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = '__all__'


class GenderSerializers(serializers.ModelSerializer):

    class Meta:
        model = Gender
        fields = '__all__'


class UserStatusSerializers(serializers.ModelSerializer):

    class Meta:
        model = UserStatus
        fields = '__all__'


class UserSerializers(serializers.ModelSerializer):
    gender = GenderSerializers()
    user_status = UserStatusSerializers()

    class Meta:
        model = User
        fields = '__all__'


class AdminSerializers(serializers.ModelSerializer):
    user = UserSerializers()

    class Meta:
        model = Admin
        fields = '__all__'


class TeacherSerializers(serializers.ModelSerializer):
    user = UserSerializers()

    class Meta:
        model = Teacher
        fields = '__all__'

class TeacherSerializer (serializers.ModelSerializer):
    teacher = TeacherSerializers()

    class Meta:
        model = User
        fields = ('teacher',)