from rest_framework import serializers
from .models import Lab

class LabSerializers1(serializers.ModelSerializer):
    lab_id = serializers.SerializerMethodField()

    class Meta:
        model = Lab
        fields = ('lab_id', 'name')

    def get_lab_id(self, obj):
        return obj['id']

