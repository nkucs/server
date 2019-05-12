from utils.api import APIView
from ..serializers import DemoSerializers1
from ..models import Demo

class DemoAPI(APIView):
    def get(self, request):
        demo_id = request.GET.get('demo_id')
        demo = Demo.objects.get(id=demo_id)
        return self.success(DemoSerializers1(demo).data)