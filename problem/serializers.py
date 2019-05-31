from rest_framework import serializers
from submission.models import Problem,ProblemSubmission,ProblemSubmissionCase
from submission.serializers import ProblemSubmissionTimeSerializers


class GetProblemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Problem
        fields = ('code', 'name', 'description', 'runtime_limit',
         'memory_limit', 'created_at','modified_at','teacher','tags')
        
