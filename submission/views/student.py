from utils.api import APIView
from rest_framework import status
from ..serializers import ProblemSubmissionSerializers1
from django.http import HttpResponse, JsonResponse
from submission.models import ProblemSubmission, CaseStatus
from lab.models import LabSubmission,Attachment
from django.forms import model_to_dict
import time; 

class GetProblemSubmissionAPI(APIView): # 获取一个学生的所有提交记录 #OK#
    def get(self, request):
        submission_problem_id = int(request.GET.get('problem_id'))
        problem_submission = ProblemSubmission.objects.filter(problem=submission_problem_id)
        caseStatusResult = CaseStatus.objects.all()
        caseStatusDemo = []
        for item in caseStatusResult:
            caseStatusDemo.append(model_to_dict(item))

        problem_submission_result = []
        for item in problem_submission:
            item_result = model_to_dict(item)
            del item_result['cases']
            item_result['create_at'] = str(item.created_at)
            item_result['status'] = caseStatusDemo[int(item_result['submission_status'])]['name']
            problem_submission_result.append(item_result)
        return self.success(problem_submission_result)

class GetAllStudentSubmissionAPI(APIView): # 获取一个学生的所有提交记录 #OK#
    def get(self, request):
        submission_student_id = int(request.GET.get('student_id'))
        student_submission = ProblemSubmission.objects.filter(student=submission_student_id)
        caseStatusResult = CaseStatus.objects.all()
        caseStatusDemo = []
        for item in caseStatusResult:
            caseStatusDemo.append(model_to_dict(item))

        student_submission_result = []
        for item in student_submission:
            item_result = model_to_dict(item)
            del item_result['cases']
            item_result['create_at'] = str(item.created_at)
            item_result['status'] = caseStatusDemo[int(item_result['submission_status'])]['name']
            student_submission_result.append(item_result)
        return self.success(student_submission_result)

class GetUserSubmissionAPI(APIView): #  获取一个学生关于一道题目的提交记录
    def get(self, request):
        submission_student_id = int(request.GET.get('student_id'))
        submission_problem_id = int(request.GET.get('problem_id'))  
        # query from database for submissions of student and problem 
        caseStatusResult = CaseStatus.objects.all()
        caseStatusDemo = []
        for item in caseStatusResult:
            caseStatusDemo.append(model_to_dict(item))

        userPersonalSubmission = ProblemSubmission.objects.filter(student=submission_student_id, problem=submission_problem_id)
        userPersonalSubmissionResult = []
        for item in userPersonalSubmission:
            item_result = model_to_dict(item)
            del item_result['cases']
            item_result['create_at'] = str(item.created_at)
            item_result['status'] = caseStatusDemo[int(item_result['submission_status'])]['name']
            userPersonalSubmissionResult.append(item_result)
        return self.success(userPersonalSubmissionResult)


class CreateProblemSubmissionAPI(APIView): #  获取一个学生关于一道题目的提交记录
    def post(self, request):
        submission_student_id = int(request.GET.get('student_id'))
        submission_problem_id = int(request.GET.get('problem_id'))
        submission_program = str(request.GET.get('program'))
        submission_create_at= time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
        submission_runtime = int(request.GET.get('runtime'))
        submission_memory = int(request.GET.get('memory'))
        submission_ip = str(request.GET.get('ip'))
        submission_language = int(request.GET.get('language'))
        submission_status_id = int(request.GET.get('status'))

        submission_result = ProblemSubmission.objects.create(
            problem=submission_problem_id,
            student=submission_student_id,
            program=submission_program,
            created_at=submission_create_at,
            runtime=submission_runtime,
            memory=submission_memory,
            Ip=submission_ip,
            language=submission_language,
            submission_status=submission_status_id,
            )

        submission_result = model_to_dict(submission_result)
        return self.success(submission_result)

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

