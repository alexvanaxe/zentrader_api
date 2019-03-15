from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from zen_fortune.serializers import ZenFortuneSerializer
from zen_fortune.models import Fortune


class ZenFortuneAPIView(APIView):
    """
    Expose the fortune service via a api call. Only get is implemented to return
    the cookie.
    """
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        fortune = Fortune()

        serializer = ZenFortuneSerializer(fortune)

        return Response(serializer.data)
