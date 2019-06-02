from rest_framework import serializers

from user.models import Student
from .models import Lab, LabProblem, LabSubmission, Attachment
from course.models import CourseResource


class LabSerializers(serializers.ModelSerializer):
    lab_id = serializers.SerializerMethodField()

    class Meta:
        model = Lab
        fields = ('lab_id', 'name')

    def get_lab_id(self, obj):
        return obj['id']


class GetLabFileSerializer(serializers.ModelSerializer):
    """
    Serialize 'resources' attribute of a Lab object.
    API: get-lab
    """

    class Meta:
        model = CourseResource
        fields = ('id', 'name')


class GetLabSerializer(serializers.ModelSerializer):
    """
    Serialize a Lab object.
    API: get-lab
    """

    files = serializers.SerializerMethodField()

    class Meta:
        model = Lab
        fields = ('name', 'description', 'start_time',
                  'end_time', 'report_required', 'files', 'attachment_weight')

    def get_files(self, obj):
        return GetLabFileSerializer(obj.resources, many=True).data


class GetLabListSerializer(serializers.ModelSerializer):
    """
    Serializer a Lab object
    API: student/lab_course_list
    """
    start_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    end_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Lab
        fields = ('name', 'start_time', 'end_time')


class LabProblemSerializer(serializers.ModelSerializer):
    """
    Serializer a Lab Problem
    API: student/lab_course_detail
    """
    name = serializers.SerializerMethodField('get_problem_name')
    id_problem = serializers.SerializerMethodField('get_problem_id')
    score = serializers.SerializerMethodField('get_problem_score')

    def get_problem_id(self, obj):
        return obj.id

    def get_problem_score(self, obj):
        lab = obj.lab
        try:
            grade = LabSubmission.objects.get(lab=lab).problem_grade
        except:
            grade = 0
        return grade

    def get_problem_name(self, obj):
        return obj.problem.name

    class Meta:
        model = LabProblem
        fields = ('name', 'score', 'id_problem')


class GetLabDetailSerializer(serializers.ModelSerializer):
    problem = LabProblemSerializer(many=True, read_only=True)
    start_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    end_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Lab
        fields = ('name', 'description', 'start_time', 'end_time', \
                  'report_required', 'problem_weight', 'attachment_weight', 'problem')


class LabSubmissionSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = LabSubmission
        fields = ('lab', 'student')


class AttachmentSerializer(serializers.Serializer):
    """
    Serialize an attachment object.
    """
    user_id = serializers.IntegerField()
    lab_id = serializers.IntegerField()
    file = serializers.FileField()

    def create(self, validated_data):
        lab = Lab.objects.get(id=validated_data.get('lab_id'))
        user = Student.objects.get(id=validated_data.get('user_id'))
        file = validated_data.get('file')
        lm = LabSubmission.objects.create(lab=lab, student=user)
        lm.save()
        am = Attachment.objects.create(lab_submission=lm, file=file)
        am.save()
        return am
