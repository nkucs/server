from rest_framework import serializers
from .models import Problem



class GetProblemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Problem
        fields = ('code', 'name', 'description', 'runtime_limit',
         'memory_limit', 'created_at','modified_at','teacher','tags')