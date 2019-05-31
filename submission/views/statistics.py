from utils.api import APIView
from ..models import ProblemSubmission, CaseStatus
from django.db.models import Q


class GetSubmissionStatAPI(APIView):

    def get(self, request):

        submission_num = dict()
        try:
            submission_status = CaseStatus.objects.all()
            submission_num[0] = ProblemSubmission.objects.filter(submission_status=submission_status[1].id).count()
            submission_num[1] = ProblemSubmission.objects.filter(~Q(submission_status=submission_status[1].id)).count()
        except ProblemSubmission.DoesNotExist:
            return self.error("error")

        return self.success(submission_num)
