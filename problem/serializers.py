from rest_framework import serializers
from .models import Problem, problem_submission, problem_submission_case



class GetProblemsSerializer(serializers.ModelSerializer):
    """
    Serialize a Lab object.
    API: get-lab
    """

    submit_count = serializers.SerializerMethodField()
    accepted_count = serializers.SerializerMethodField()

    class Meta:
        model = Problem
        fields = ('id', 'name', 'id_teacher', 'created_at', 'submit_count', 'accepted_count')

    def get_submit_count(self, obj):
        return problem_submission.objects.filter(id_problem=obj.id).count()

    def get_accepted_count(self, obj):
        id_problem_submission = problem_submission.objects.get(id_problem=obj.id)[0]['id']
        sub_count = problem_submission.objects.filter(id_problem=obj.id).count()
        un_ac_count = problem_submission_case.objects.filter(id_problem_submission=id_problem_submission).count()
        return  sub_count - un_ac_count