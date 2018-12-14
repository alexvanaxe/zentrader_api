from datetime import datetime

from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse

from operation.models import Operation
from account.unit_tests.account_mocks import create_account
from stock.unit_tests.stock_mocks import create_stocks
from operation.unit_tests.operation_mocks import create_operations


class OperationTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        create_account(cls)
        create_stocks(cls)
        create_operations(cls, cls.stock)


class OperationTest(OperationTestCase):

    def test_patch(self):
        """ Verify that a patch update is possible. """
        url = reverse('experience-detail', kwargs={'pk': self.operation.pk})
        response = self.client.patch(url, {"amount": 200})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['amount'], "200")

    def test_get(self):
        """ Verify that everything is correct in the configuration """
        url = reverse('experience-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(len(response.data)), '2')
        # self.assertEqual(response.data[0]["stock"]['code'], "XPTO3")

    def get_archived(self):
        """ Verify that the application doesnt return the archived opperations """
        url = reverse('experience-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data[0]["price"]), "30.00")

    def test_archive(self):
        """ Verify that the archive functionalitty works fine """
        self.assertFalse(self.operation.archived)
        url = reverse('archive', kwargs={'pk': self.operation.pk})

        response = self.client.patch(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['archived'])
        operation_updated = Operation.objects.get(pk=self.operation.pk)
        self.assertTrue(operation_updated.archived)


    def test_delete(self):
        """ Verify that a delete is possible. """
        url = reverse('experience-detail', kwargs={'pk': self.operation.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def method_call(self):
        url = reverse('operation-cost', kwargs={'pk': self.operation.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data['cost']), '30000.00')


class ExperienceDataTest(OperationTestCase):
    def test_post(self):
        url = reverse('experience-list')
        response = self.client.post(url, {'stock': self.stock.pk,
                                          'amount': '200',
                                          'price': '10',
                                          'target': '40.00'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_archived(self):
        url = reverse('experience-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(len(response.data)), '2')

    def patch_nested(self):
        """ Test if the patch is possible with a nested operation """
        url = reverse('experience-detail', kwargs={'pk': self.experience.pk})
        response = self.client.patch(url, {'stop_gain': 36})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data['stop_gain']), '36.00')

    def test_gain(self):
        url = reverse('experience-detail', kwargs={'pk': self.experience.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data['target_gain']), '-10020.01')

    def test_gain2(self):
        url = reverse('experience-detail', kwargs={'pk': self.experience.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual("{0:.2f}".format(response.data['operation_limit']), '31.00')


class BuyDataTest(OperationTestCase):
    def test_validation_buy(self):
        url = reverse('buy-list')
        response = self.client.post(url, {'stock': self.stock.pk,
                                          'amount': '200000',
                                          'price': '1000',
                                          'target': '40.00'})

        self.assertEqual(response.status_code, status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE)


class SellDataTest(OperationTestCase):
    def test_validation_amount_before_execution(self):
        """
        This should pass ok
        """
        url = reverse('sell-list')
        response = self.client.post(url, {'stock': self.stock.pk,
                                          'buy': self.buy3.pk,
                                          'amount': '200000',
                                          'price': '1000',
                                          'target': '40.00'})

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
                                          'executed': True})

        self.assertEqual(response.status_code, status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE)

    def test_sell_data_update_executed(self):
        url = reverse('sell-detail', kwargs={'pk': self.sell2.pk})
        response = self.client.patch(url, {'amount': 50})

        self.assertEqual(response.status_code, status.HTTP_423_LOCKED)

        url = reverse('sell-detail', kwargs={'pk': self.sell3.pk})
        response = self.client.patch(url, {'amount': 50, 'executed': False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('sell-detail', kwargs={'pk': self.sell3.pk})
        response = self.client.patch(url, {'amount': 150, 'executed': True})
        self.assertEqual(response.status_code, status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE)

        url = reverse('sell-detail', kwargs={'pk': self.sell3.pk})
        response = self.client.patch(url, {'amount': 50, 'executed': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

