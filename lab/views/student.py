from rest_framework import status
from rest_framework.response import Response

from utils.api import APIView
from ..models import Lab
from ..models import LabProblem
from course.models import Course
from ..serializers import GetLabListSerializer, GetLabDetailSerializer, AttachmentSerializer


class LabAPI(APIView):
    def get(self, request):
        id_course = request.GET.get('id_course')
        print(id_course)
        if id_course:
            try:
                course = Course.objects.get(id=id_course)
            except:
                return self.error(msg="不存在该课程", err=400)
            labs = Lab.objects.filter(course=course)
            serializer = GetLabListSerializer(labs, many=True)
            return self.success(serializer.data)
        else:
            return self.error(msg="参数错误", err=400)


class LabDetailAPI(APIView):
    def get(self, request):
        id_lab = request.GET.get('id_lab')
        if id_lab:
            # try:
            lab = Lab.objects.get(id=id_lab)
            return self.success(GetLabDetailSerializer(lab).data)
            # except:
            #     return self.error(msg="不存在该实验", err=400)
        else:
            return self.error(msg="参数错误", err=400)


class ProblemHandInAPI(APIView):
    def get(self, request):
        # problem_list = request.GET.get('problem_list')
        # problem_data = LabProblem.objects.all()
        # return self.success(GetLabDetailSerializer(problem_data).data)
        return self.success("我成功了！")

class PostAttachmentAPI(APIView):
    """
    学生在网页上传文件点击提交后，新增一条Attachment记录
    API: post-attachment
    """
    def post(self, request):
        serializer = AttachmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return self.error(msg="参数错误", err=400)
