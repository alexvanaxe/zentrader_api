from rest_framework import views, response

from operation.models import Operation
from operation.serializers import ArchiveSerializer


class ArchiveApiView(views.APIView):
    """ Api to archive an operation. Used when we cannot save it in the interface
    but want to archive it.
    """
    def patch(self, request, pk, format=None):
        instance = Operation.objects.get(pk=pk)
        serializer = ArchiveSerializer(instance)
        serializer.save(instance)

        return response.Response(serializer.data)
