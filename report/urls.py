from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from report.views import TotalProfitReportView

urlpatterns = [
    url(r'^report/total_profit/$', TotalProfitReportView.as_view(), name="total-profit-retrieve"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
