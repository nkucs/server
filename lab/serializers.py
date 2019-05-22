from rest_framework import serializers
from .models import Lab

class LabSerializers1(serializers.ModelSerializer):
    lab_id = serializers.SerializerMethodField()
    # name = serializers.CharField()
    # id = serializers.CharField()

    class Meta:
        model = Lab
        fields = ('lab_id', 'name')

    def get_lab_id(self, obj):
        return obj['id']

# class DemoSerializers2(serializers.ModelSerializer):

#     class Meta:
#         model = Lab
#         fields = ('content', 'is_public')
#         # or  fields = '__all__'
