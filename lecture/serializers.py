from rest_framework import serializers
from .models import Lecture
from course.models import CourseResource
from problem.models import Problem


class LectureSerializers(serializers.ModelSerializer):
    lecture_id = serializers.SerializerMethodField()

    class Meta:
        model = Lecture
        fields = ('lecture_id', 'name')

    def get_lecture_id(self, obj):
        return obj['id']

class GetLectureFileSerializer(serializers.ModelSerializer):
    """
    Serialize 'resources' attribute of a Lecture object.
    API: get-lecture
    """

    class Meta:
        model = CourseResource
        fields = ('id', 'name')

class GetLectureProblemSerializer(serializers.ModelSerializer):
    """
    Serialize 'problems' attribute of a Lecture object.
    API: get-lecture
    """

    class Meta:
        model = Problem
        fields = ('id', 'name')

class GetLectureSerializer(serializers.ModelSerializer):
    """
    Serialize a Lecture object.
    API: get-lecture
    """

    files = serializers.SerializerMethodField()
    problems = serializers.SerializerMethodField()

    class Meta:
        model = Lecture
        fields = ('name', 'description', 'files', 'problems')

    def get_files(self, obj):
        return GetLectureFileSerializer(obj.resources, many=True).data
    
    def get_problems(self, obj):
        return GetLectureProblemSerializer(obj.resources, many=True).data

