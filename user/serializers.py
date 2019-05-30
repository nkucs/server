from rest_framework import serializers
from .models import Role, User
from django.db.utils import IntegrityError


class RoleSerializers(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
