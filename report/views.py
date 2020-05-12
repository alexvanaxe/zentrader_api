from rest_framework.views import APIView
from rest_framework.response import Response

from report.models import Report
from report.serializers import ReportTotalProfitSerializer


class TotalProfitReportView(APIView):
    """
    Return the total profit, considering all executed operations
    """
    def get(self, request, format=None):
        report = Report()

        serializer = ReportTotalProfitSerializer(report)

        return Response(serializer.data)
