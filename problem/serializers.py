from rest_framework import serializers
from submission.models import Problem,ProblemSubmission,ProblemSubmissionCase
from submission.serializers import ProblemSubmissionTimeSerializers
from user.models import Teacher
from .models import Case,Tag
     
class GetTeacherSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Teacher
        fields = '__all__'


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
        return ProblemSubmission.objects.filter(problem=obj.id).count()//2


class GetTagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'name')

class GetProblemSerializer(serializers.ModelSerializer):
    cases = serializers.ReadOnlyField()
    tags = GetTagsSerializer(many=True)
    class Meta:
        model = Problem
        fields = ('name', 'description', 'teacher','runtime_limit',
         'memory_limit', 'created_at','modified_at','tags','cases')


class GetCasesSerializer(serializers.ModelSerializer):
    tags = GetTagsSerializer(many=True)
    class Meta:
        model = Case
        fields = ('id', 'input', 'output','tags')

class GetOneProblemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Problem
        fields = ('id','name', 'description', 'teacher','runtime_limit',
         'memory_limit', 'created_at','modified_at','tags')

