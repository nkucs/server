from utils.api import APIView
from ..models import ProblemSubmission, CaseStatus
from django.db.models import Q

from utils.api import APIView, JSONResponse
from rest_framework import status
from ..serializers import ProblemSubmissionSerializers1
from django.http import HttpResponse, JsonResponse
from ..models import ProblemSubmission, CaseStatus
from problem.models import Problem, Tag
from lecture.models import Lecture

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


def get_tags(problem_id):
    word_tags = Problem.objects.get(id=problem_id)
    problem_tags = list()
    for tag in word_tags.tags.all():
        problem_tags.append(tag.name)
    return problem_tags


class GetWordCloud(APIView):
    def get(self, request):
        course_id = request.GET.get("course_id")
        problems = Lecture.objects.get(id=course_id).problems.all()
        # problems = ProblemSubmission.objects.all().values('id')
        status_obj = ProblemSubmission.objects.filter()
        status_list = self.get_status(status_obj)

        j = 0
        tags_dict_ac = dict()
        tags_dict_not_ac = dict()
        for p_id in problems:
            tags_list = get_tags(p_id.id)
            if status_list[j]:
                for tag in tags_list:
                    if tag not in tags_dict_ac.keys():
                        tags_dict_ac[tag] = 0
                    tags_dict_ac[tag] += 1
            else:
                for tag in tags_list:
                    if tag not in tags_dict_not_ac.keys():
                        tags_dict_not_ac[tag] = 0
                    tags_dict_not_ac[tag] += 1
            j += 1

        wordcloud_data_ac = list()
        wordcloud_data_not_ac = list()
        for dic in tags_dict_ac:
            temp = dict()
            temp['word'] = dic
            temp['count'] = tags_dict_ac[dic]
            wordcloud_data_ac.append(temp)
        for dic in tags_dict_not_ac:
            temp = dict()
            temp['word'] = dic
            temp['count'] = tags_dict_not_ac[dic]
            wordcloud_data_not_ac.append(temp)
        words = [wordcloud_data_ac, wordcloud_data_not_ac]
        return JsonResponse(words, status=status.HTTP_200_OK, safe=False)

    def get_status(self, status_obj):
        status_list = []
        for st in status_obj:
            flag = True
            cases = st.submission_status.name
            for seq in cases:
                if seq == '0':
                    flag = False
                    break
            status_list.append(flag)
        return status_list
