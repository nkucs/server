from rest_framework import serializers
from .models import Lab
from course.models import CourseResource


class LabSerializers(serializers.ModelSerializer):
    lab_id = serializers.SerializerMethodField()

    class Meta:
        model = Lab
        fields = ('lab_id', 'name')

    def get_lab_id(self, obj):
        return obj['id']


class GetLabFileSerializer(serializers.ModelSerializer):
    """
    Serialize 'resources' attribute of a Lab object.
    API: get-lab
    """

    class Meta:
        model = CourseResource
        fields = ('id', 'name')


class GetLabSerializer(serializers.ModelSerializer):
    """
    Serialize a Lab object.
    API: get-lab
    """

    files = serializers.SerializerMethodField()

    class Meta:
        model = Lab
        fields = ('name', 'description', 'start_time',
                  'end_time', 'report_required', 'files')

    def get_files(self, obj):
        return GetLabFileSerializer(obj.resources, many=True).data
