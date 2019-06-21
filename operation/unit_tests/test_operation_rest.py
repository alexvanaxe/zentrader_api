from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse

from operation.models import Operation
from account.unit_tests.account_mocks import create_account
from stock.unit_tests.stock_mocks import create_stocks
from zen_oauth.unit_tests.user_mocks import create_test_user, create_auth
from operation.unit_tests.operation_mocks import create_operations


class OperationTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        create_test_user(cls)
        create_auth(cls, cls.user)
        create_account(cls)
        create_stocks(cls)
        create_operations(cls, cls.stock, cls.user)


class OperationTest(OperationTestCase):
    def test_archive(self):
        """ Verify that the archive functionalitty works fine """
        self.assertFalse(self.operation.archived)
        url = reverse('archive', kwargs={'pk': self.operation.pk})

        response = self.client.patch(url, HTTP_AUTHORIZATION=self.auth)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['archived'])
        operation_updated = Operation.objects.get(pk=self.operation.pk)
        self.assertTrue(operation_updated.archived)

    def method_call(self):
        url = reverse('operation-cost', kwargs={'pk': self.operation.pk})
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data['cost']), '30000.00')
