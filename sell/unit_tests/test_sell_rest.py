from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse

from account.unit_tests.account_mocks import create_account
from stock.unit_tests.stock_mocks import create_stocks
from zen_oauth.unit_tests.user_mocks import create_test_user, create_auth
from operation.unit_tests.operation_mocks import create_operations


class SellTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        create_test_user(cls)
        create_auth(cls, cls.user)
        create_account(cls)
        create_stocks(cls)
        create_operations(cls, cls.stock, cls.user)


class SellDataTest(SellTestCase):
    def test_validation_amount_before_execution(self):
        """
        This should pass ok
        """
        url = reverse('sell-list')
        response = self.client.post(url, {'stock': self.stock.pk,
                                          'buy': self.buy3.pk,
                                          'amount': '200000',
                                          'price': '1000',
                                          'target': '40.00'}, HTTP_AUTHORIZATION=self.auth)

        self.assertEqual(response.status_code, status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE)

    def test_validation_amount_executing(self):
        """
        This should pass ok
        """
        url = reverse('sell-list')
        response = self.client.post(url, {'stock': self.stock.pk,
                                          'buy': self.buy3.pk,
                                          'amount': '200000',
                                          'price': '1000',
                                          'target': '40.00',
                                          'executed': True}, HTTP_AUTHORIZATION=self.auth)

        self.assertEqual(response.status_code, status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE)

    def test_sell_data_update_executed(self):
        url = reverse('sell-detail', kwargs={'pk': self.sell2.pk})
        response = self.client.patch(url, {'amount': 50}, HTTP_AUTHORIZATION=self.auth)

        self.assertEqual(response.status_code, status.HTTP_423_LOCKED)

        url = reverse('sell-detail', kwargs={'pk': self.sell3.pk})
        response = self.client.patch(url, {'amount': 50, 'executed': False}, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('sell-detail', kwargs={'pk': self.sell3.pk})
        response = self.client.patch(url, {'amount': 150, 'executed': True}, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE)

        url = reverse('sell-detail', kwargs={'pk': self.sell3.pk})
        response = self.client.patch(url, {'amount': 50, 'executed': True}, HTTP_AUTHORIZATION=self.auth)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
