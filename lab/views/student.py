from utils.api import APIView
from ..models import Lab
from course.models import Course
from ..serializers import GetLabListSerializer,GetLabDetailSerializer


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
