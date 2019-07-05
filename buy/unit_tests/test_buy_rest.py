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


class BuyDataTest(SellTestCase):
    def test_validation_buy(self):
        url = reverse('buy-list')
        response = self.client.post(url, {'stock': self.stock.pk,
                                          'amount': '200000',
                                          'price': '1000',
                                          'target': '40.00'}, HTTP_AUTHORIZATION=self.auth)

        self.assertEqual(response.status_code, status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE)

    def test_filter_by_experimence(self):
        url = reverse('buy-list')
        response = self.client.get(url + '?archived=false&experience=' + str(self.experience.pk), HTTP_AUTHORIZATION=self.auth)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(len(response.data)), '1')
