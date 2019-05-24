from rest_framework import serializers
from .models import Lecture

class LectureSerializers(serializers.ModelSerializer):
    lecture_id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    class Meta:
        model = Lecture
        fields = ('lecture_id', 'name')
    def get_lecture_id(self, obj):
        return obj['id']
    def get_name(self, obj):
        return obj['name']