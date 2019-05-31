from rest_framework import serializers
from .models import Problem 
from submission.models import ProblemSubmission, ProblemSubmissionCase


class GetProblemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Problem
        fields = ('code', 'name', 'description', 'runtime_limit',
         'memory_limit', 'created_at','modified_at','teacher','tags')
        
class GetProblemsSerializer(serializers.ModelSerializer):
    """
    Serialize a Lab object.
    API: get-lab
    """

    submit_count = serializers.SerializerMethodField()
    accepted_count = serializers.SerializerMethodField()

    class Meta:
        model = Problem
        fields = ('id', 'name', 'teacher', 'created_at', 'submit_count', 'accepted_count')

    def get_submit_count(self, obj):
        #return '70'
        return ProblemSubmission.objects.filter(problem=obj.id).count()

    def get_accepted_count(self, obj):
        #id_problem_submission = ProblemSubmission.objects.filter(problem=obj.id)[0].id
        #sub_count = ProblemSubmission.objects.filter(problem=obj.id).count()
        #un_ac_count = ProblemSubmissionCase.objects.filter(problem_submission=id_problem_submission).count()
        #return  sub_count - un_ac_count
        #return '20'
        return ProblemSubmission.objects.filter(problem=obj.id).count()/2