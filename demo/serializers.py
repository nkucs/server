from rest_framework import serializers
from .models import Demo

class DemoSerializers1(serializers.Serializer):
    content = serializers.CharField()

class DemoSerializers2(serializers.ModelSerializer):

    class Meta:
        model = Demo
        fields = ('content', 'is_public')
        # or  fields = '__all__'