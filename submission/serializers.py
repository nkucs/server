from rest_framework import serializers
from .models import ProblemSubmission

class ProblemSubmissionSerializers1(serializers.ModelSerializer):
    class Meta:
        model = ProblemSubmission
        fields = ('id', 'problem', 'student', 'program', 
        'created_at', 'runtime', 'memory','IP','language','cases','lectures')

