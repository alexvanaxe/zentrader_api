from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from report.views import TotalProfitReportView, TotalProfitMonthlyReportView

urlpatterns = [
    path('report/total_profit/', TotalProfitReportView.as_view(),
        name="total-profit-retrieve"),

    path('report/total_profit_monthly/',
        TotalProfitMonthlyReportView.as_view(),
        name="total-profit-monthly-retrieve"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
