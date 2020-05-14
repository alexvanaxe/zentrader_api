from django.test.testcases import TestCase
from django.core.cache import cache
from datetime import datetime

from stock.unit_tests.stock_mocks import create_stocks
from account.unit_tests.account_mocks import create_account
from operation.unit_tests.operation_mocks import create_operations,\
                                                 create_recent_sells
from zen_oauth.unit_tests.user_mocks import create_test_user, create_auth

from report.models import Report


class ReportModelTestCase(TestCase):
    """
    Base report class to setup the tests.
    """
    @classmethod
    def setUpTestData(cls):
        cache.clear()
        create_test_user(cls)
        create_auth(cls, cls.user)
        create_account(cls)
        create_stocks(cls)


class ReportProfit(ReportModelTestCase):
    """
    Test the profits reports.
    """
    def test_total_profit(self):
        report = Report()
        create_operations(self, self.stock, self.user)

        self.assertEqual("{0:.2f}".format(report.total_profit()), "665.96")

    def test_total_profit_by_month(self):
        report = Report()
        create_recent_sells(self, self.stock, self.user)
        monthly_profit = report.total_monthly_profit()
        cur_month = datetime.now().month

        self.assertEqual("{0:.2f}".format(monthly_profit[cur_month]), "679.96")
        self.assertEqual("{0:.2f}".format(monthly_profit[3]), "0.00")
