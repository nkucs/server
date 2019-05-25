from rest_framework import serializers
from .models import Role
from django.db.utils import IntegrityError


class RoleSerializers(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = '__all__'
