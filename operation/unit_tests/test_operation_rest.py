from rest_framework.test import APITestCase
from rest_framework import status

from django.core.urlresolvers import reverse

from account.unit_tests.account_mocks import create_account
from stock.unit_tests.stock_mocks import create_stocks
from operation.unit_tests.operation_type_mocks import create_operation_types
from operation.unit_tests.operation_mocks import create_operations


class OperationTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        create_stocks(cls)
        create_account(cls)
        create_operation_types(cls)
        create_operations(cls, cls.stock, cls.operationType)


class OperationTest(OperationTestCase):

    def test_post(self):
        """ Verify that everything is correct in the configuration """
        url = reverse('operation-list')
        response = self.client.post(url, {'stock': self.stock.pk, 'operation_type': self.operationType.pk,
                                          'date': '2017-07-04T15:58:58.782', 'amount': 1000, 'price': '15.00'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get(self):
        """ Verify that everything is correct in the configuration """
        url = reverse('operation-nested-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["stock"]['code'], "XPTO3")

    def test_method_call(self):
        url = reverse('operation-cost', kwargs={'pk': self.operation.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data['cost']), '30000.00')


class ExperienceDataTest(OperationTestCase):
    def test_post(self):
        url = reverse('experience-list')
        response = self.client.post(url, {'operation': self.operation.pk, 'target': '40.00'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_gain(self):
        url = reverse('experience-detail', kwargs={'pk': self.experience.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data['operation_gain']), '-10019.99')

    def test_gain(self):
        url = reverse('experience-detail', kwargs={'pk': self.experience.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data['operation_limit']), '28.28')