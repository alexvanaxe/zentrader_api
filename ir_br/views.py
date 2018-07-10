"""
View that retrieves and returns the ir of the current month
"""
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response

from ir_br.models import IrBrManager, IrBr
from ir_br.serializers import IrBrSerializer

class IrBrApiView(APIView):
    """
    View that retrieves the ir to pay
    """
    def get(self, request, format=None):
        ir = IrBrManager().retrieveIr()

        serializer = IrBrSerializer(ir)

        return Response(serializer.data)


class IrBrApiGetView(APIView):
    """
    View that retrieves the ir to pay
    """
    def get(self, request, date, format=None):
        ir = IrBrManager().retrieveIr(datetime.strptime(date,'%Y-%m-%dT%H:%M:%S'))

        serializer = IrBrSerializer(ir)

        return Response(serializer.data)
