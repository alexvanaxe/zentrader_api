from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse

from operation.unit_tests.operation_mocks import create_operations
from stock.unit_tests.stock_mocks import create_stocks
from account.unit_tests.account_mocks import create_account
from zen_oauth.unit_tests.user_mocks import create_test_user, create_auth


class ReportTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        create_test_user(cls)
        create_auth(cls, cls.user)
        create_account(cls)
        create_stocks(cls)
        create_operations(cls, cls.stock, cls.user)


class ReportTest(ReportTestCase):
    def test_report_total_profit(self):
        url = reverse('total-profit-retrieve')
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data['total_profit']), '665.96')
