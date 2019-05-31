from utils.api import APIView
from rest_framework import status
from ..serializers import ProblemSubmissionSerializers1
from django.http import HttpResponse, JsonResponse
from submission.models import ProblemSubmission
from lab.models import LabSubmission,Attachment

class GetAllSubmissionAPI(APIView): # 获取一个学生的所有提交记录
    def get(self, request):
        # submission_student_id = int(request.GET.get('submission_student_id'))
        # query from database for submissions of student
        # id_student=submission_student_id
        # try:
        print("@@@@@@@@@@@@@@@@")
        UserPersonalSubmission = str(ProblemSubmission.objects.count())
        # except UserPersonalSubmission.DoesNotExist:
        #     return HttpResponse(status=404)
        serializer = ProblemSubmissionSerializers1(UserPersonalSubmission)
        return JsonResponse(serializer.data,status=status.HTTP_200_OK)

class GetUserSubmissionAPI(APIView): #  获取一个学生关于一道题目的提交记录
    def get(self, request):
        submission_student_id = int(request.GET.get('submission_student_id'))
        submission_problem_id = int(request.GET.get('submission_problem_id'))
        # query from database for submissions of student and problem 
        try:
            UserPersonalSubmission = ProblemSubmission.objects.filter(id_student=submission_student_id, id_problem=submission_problem_id)
        except ProblemSubmission.DoesNotExist:
            return HttpResponse(status=404)
        serializer = ProblemSubmissionSerializers1(ProblemSubmission)
        return JsonResponse(serializer.data,status=status.HTTP_200_OK)

class AddLabAttachmentAPI(APIView):
    # create submission of a lab
    def post(self, request):
        submission_student_id = int(request.GET.get('id_user'))
        course_id = int(request.GET.get('id_course'))
        lab_id = int(request.GET.get('id_lab'))
        attachment_path = int(request.GET.get('file'))
        # query from database for submissions of student and problem 
        try:
            labSubmission = LabSubmission.objects.filter(id_student=submission_student_id, id_lab=lab_id)
        except ProblemSubmission.DoesNotExist:
            return HttpResponse(status=404)
        try:
            attachment = Attachment.objects.create(
                id_lab_submission = labSubmission.id,
                path = attachment_path
            )
        except Exception as e:
            return HttpResponse(status=-1)
        return HttpResponse(status=0)

