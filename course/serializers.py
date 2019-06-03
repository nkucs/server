from rest_framework import serializers
from .models import Course
from user.models import Student

class CourseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
