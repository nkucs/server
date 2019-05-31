from rest_framework import serializers
from .models import ProblemSubmission,ProblemSubmissionCase
from user.models import Student


class ProblemSubmissionSerializers1(serializers.ModelSerializer):
    class Meta:
        model = ProblemSubmission
        fields = ('id', 'problem', 'student', 'program', 
        'created_at', 'runtime', 'memory','IP','language','cases','lectures')

class ProblemSubmissionTimeSerializers(serializers.ModelSerializer):

    all_cases_count = serializers.ReadOnlyField()
    succeed_cases_count= serializers.ReadOnlyField()
    student_number = serializers.StringRelatedField()
    class Meta:
        model = ProblemSubmission
        fields = ('id', 'problem', 'student','student_number','all_cases_count','succeed_cases_count','created_at','language')





