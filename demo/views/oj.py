from rest_framework.permissions import IsAuthenticated

from utils.api import APIView
from ..serializers import DemoSerializers1
from ..models import Demo


class DemoAPI(APIView):
    # Add the following line for authentication purposes.
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        demo_id = request.GET.get('demo_id')
        demo = Demo.objects.get(id=demo_id)
        return self.success(DemoSerializers1(demo).data)
