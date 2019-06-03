import datetime
import math
import time

import pytz
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from rest_framework import status

from course.models import Course
from lecture.models import Lecture, LectureProblem
from problem.models import Problem, Tag
from utils.api import APIView, JSONResponse

from ..models import CaseStatus, ProblemSubmission, ProblemSubmissionCase
from ..serializers import ProblemSubmissionSerializers1


class GetSubmissionStatAPI(APIView):

    def get(self, request):

        submission_num = dict()
        try:
            submission_status = CaseStatus.objects.all()
            submission_num[0] = ProblemSubmission.objects.filter(
                submission_status=submission_status[1].id).count()
            submission_num[1] = ProblemSubmission.objects.filter(
                ~Q(submission_status=submission_status[1].id)).count()
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
        courses = Course.objects.get(id=course_id)
        lectures = Lecture.objects.get(course=courses)
        problems = lectures.problems.all()
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


def judge_AC(case_status):
    """判断CaseStatus_id对应的测试案例通过情况"""
    status_list = case_status.name
    for status in status_list:
        if status is '0':
            return False
    return True


def get_submission_count_by_day(required_submissions):
    day_count = {'total': [0]*12, 'AC': [0]*12, 'not_AC': [0]*12}
    now = datetime.datetime.now()
    zero_today = now - datetime.timedelta(
        hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
    submissions = required_submissions.filter(created_at__gt=zero_today)
    for submission in submissions:
        day_count['total'][submission.created_at.hour//2] += 1
        if judge_AC(submission.submission_status):
            day_count['AC'][submission.created_at.hour//2] += 1
        else:
            day_count['not_AC'][submission.created_at.hour//2] += 1
    return day_count


def get_submission_count_by_week(required_submissions):
    total_count = dict()
    AC_count = dict()
    not_AC_count = dict()
    week_count = {'total': total_count, 'AC': AC_count, 'not_AC': not_AC_count}
    now = datetime.datetime.now()
    for i in range(-6, 1):
        day = now + datetime.timedelta(days=i)
        day_format = day.strftime('%Y-%m-%d')
        total_count[day_format] = 0
        AC_count[day_format] = 0
        not_AC_count[day_format] = 0
    zero_today = now - datetime.timedelta(
        hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
    zero_end = zero_today + datetime.timedelta(hours=24)
    zero_start = zero_end - datetime.timedelta(hours=24*7)
    submissions = required_submissions.filter(created_at__gt=zero_start)
    for submission in submissions:
        day = submission.created_at.strftime('%Y-%m-%d')
        total_count[day] += 1
        if judge_AC(submission.submission_status):
            AC_count[day] += 1
        else:
            not_AC_count[day] += 1
    return week_count


def get_submission_count_by_month(required_submissions):
    month_count = {'total': [0]*12, 'AC': [0]*12, 'not_AC': [0]*12}
    now = datetime.datetime.now()
    print(now.year)
    zero_start = datetime.datetime(
        year=now.year, month=1, day=1, hour=0, minute=0, second=0)
    submissions = required_submissions.filter(created_at__gt=zero_start)
    for submission in submissions:
        month_count['total'][submission.created_at.month-1] += 1
        if judge_AC(submission.submission_status):
            month_count['AC'][submission.created_at.month-1] += 1
        else:
            month_count['not_AC'][submission.created_at.month-1] += 1
    return month_count


def get_submission_count_by_year(required_submissions):
    total_count = dict()
    AC_count = dict()
    not_AC_count = dict()
    year_count = {'total': total_count, 'AC': AC_count, 'not_AC': not_AC_count}
    now = datetime.datetime.now()
    this_year = now.year
    for year_offset in range(-4, 1):
        total_count[this_year+year_offset] = 0
        AC_count[this_year+year_offset] = 0
        not_AC_count[this_year+year_offset] = 0
    zero_start = datetime.datetime(
        year=now.year-4, month=1, day=1, hour=0, minute=0, second=0, tzinfo=pytz.UTC)
    submissions = required_submissions.filter(created_at__gt=zero_start)
    for submission in submissions:
        total_count[submission.created_at.year] += 1
        if judge_AC(submission.submission_status):
            AC_count[submission.created_at.year] += 1
        else:
            not_AC_count[submission.created_at.year] += 1
    return year_count


class GetSubmissionCountAPI(APIView):
    response_class = JSONResponse

    def get(self, request):
        date_range = request.GET.get('date_range')
        course_id = request.GET.get('course_id')
        course = Course.objects.get(id=course_id)
        lectures = Lecture.objects.filter(course=course)
        required_submissions = lectures[0].problem_submissions.all()
        for lecture in lectures[1:]:
            required_submissions.extend(lecture.problem_submissions.all())
        if date_range == 'day':
            day_count = get_submission_count_by_day(required_submissions)
            return self.success(day_count)
        elif date_range == 'week':
            week_count = get_submission_count_by_week(required_submissions)
            return self.success(week_count)
        elif date_range == 'month':
            month_count = get_submission_count_by_month(required_submissions)
            return self.success(month_count)
        elif date_range == 'year':
            year_count = get_submission_count_by_year(required_submissions)
            return self.success(year_count)


class GetSubmissionTags(APIView):

    def get(self, request):
        response = dict()
        course_id = request.GET.get("course_id")
        try:
            lectures = Lecture.objects.filter(course_id=course_id)
        except Lecture.DoesNotExist:
            return self.error("error")
        problems = []
        for lecture in lectures:
            for rel in LectureProblem.objects.filter(lecture_id=lecture.id):
                problems.append(rel.problem)
        submissions = []
        for problem in problems:
            for rel in ProblemSubmission.objects.filter(problem_id=problem.id):
                submissions.append(rel)
        submissionCases = []
        for submission in submissions:
            for rel in ProblemSubmissionCase.objects.filter(
                    problem_submission_id=submission.id):
                submissionCases.append(rel)

        Case1 = CaseStatus.objects.get(name="通过")

        response['ans'] = []
        tags_name = []
        for subCase in submissionCases:
            tags = subCase.case.tags
            for tag in tags.all():
                name = tag.name
                if name not in tags_name:
                    tags_name.append(name)
                    response['ans'].append(
                        {'标签': name, '通过数': 0, '未通过数': 0, '总数': 0})
                index = tags_name.index(name)
                if subCase.case_status_id == Case1.id:
                    response['ans'][index]['通过数'] += 1
                response['ans'][index]['总数'] += 1
        for raw in response['ans']:
            raw['未通过数'] = raw['总数'] - raw['通过数']

        return JsonResponse(response, status=status.HTTP_200_OK, safe=False)


class GetSubmissionInfoAPI(APIView):

    def get(self, request):
        response = []
        problem_ids = {}
        course_id = request.GET.get("course_id")
        try:
            lectures = Lecture.objects.filter(course_id=course_id)
        except Lecture.DoesNotExist:
            return self.error("error")
        required_submissions = []
        index = 0
        for lecture in lectures:
            print(lecture.id, 'ddddd')
            required_submissions.extend(lecture.problem_submissions.all())
            for rel in LectureProblem.objects.filter(lecture_id=lecture.id):
                # print(rel.id, 'cccc')
                rel_problem = rel.problem
                problem = dict()
                if rel_problem.id not in problem_ids:
                    problem_ids[rel_problem.id] = index
                    index += 1
                    problem['problem_id'] = rel_problem.id
                    problem['problem_name'] = rel_problem.name
                    problem['start_time'] = rel_problem.created_at.strftime(
                        '%Y-%m-%d %H:%M:%S')
                    problem['update_time'] = rel_problem.modified_at.strftime(
                        '%Y-%m-%d %H:%M:%S')
                    problem['submit_times'] = 0
                    problem['AC_times'] = 0
                    response.append(problem)
        for submission in required_submissions:
            problem = submission.problem
            response[problem_ids[problem.id]]['submit_times'] += 1
            if judge_AC(submission.submission_status):
                response[problem_ids[problem.id]]['AC_times'] += 1
        for problem in response:
            try:
                problem['ACrate'] = str(
                    problem['AC_times'] / problem['submit_times'] * 100) + '%'
            except:
                problem['ACrate'] = '0.0%'
        return JsonResponse(response, status=status.HTTP_200_OK, safe=False)


class GetSubmissionDistributionAPI(APIView):
    def get(self, request):
        print(request)
        if 'start_date' not in request.GET or \
           'end_date' not in request.GET or \
           'student_id' not in request.GET:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        student_id = request.GET['student_id']
        start_time = request.GET['start_date']
        end_time = request.GET['end_date']
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d")
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d")
        submission = ProblemSubmission.objects.filter(
            student=student_id, created_at__range=[start_time, end_time])
        counts = []
        t = datetime.time()
        for i in range(0, 22, 2):
            subm = submission.filter(
                created_at__time__range=[datetime.time(i), datetime.time(i+2)])
            counts.append((subm.count(), subm.filter(submission_status=0).count()))
        temp = {}
        temp['ans'] = []
        for i, c in enumerate(counts):
            t = {}
            t["时间段"] = f"{i*2}:00-{(i+1)*2}:00"
            t["提交数"] = counts[i][0]
            t["AC数"] = counts[i][1]
            temp['ans'].append(t)
        return JsonResponse(temp, status=status.HTTP_200_OK)


class GetACSubmissionRuntimes(APIView):
    def get(self, request):
        problem_id = request.GET.get('problem_id')
        problemSubmission = ProblemSubmission.objects.filter(problem=problem_id).order_by('runtime')
        num = problemSubmission.count()
        if (problemSubmission.count() < 1):
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        maxtime = problemSubmission.last().runtime
        interval = math.ceil(maxtime/10)
        # i = 0
        data = []

        for i in range(0, maxtime, interval):
            count = problemSubmission.filter(
                runtime__range=(i, i+interval)).count()
            data.append(count/num)
        send = {'interval': interval, 'data': data}
        return JsonResponse(send, status=status.HTTP_200_oK)
