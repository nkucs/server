from rest_framework import serializers
from course.models import Course

class CourseSerializer(serializers.ModelSerializer):
    class meta:
        model = Course
        fields = ('id','name', 'start_time', 'end_time',
         'description')