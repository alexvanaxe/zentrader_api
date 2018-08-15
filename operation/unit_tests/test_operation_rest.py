from datetime import datetime

from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse

from account.unit_tests.account_mocks import create_account
from stock.unit_tests.stock_mocks import create_stocks
from operation.unit_tests.operation_mocks import create_operations


class OperationTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        create_account(cls)
        create_stocks(cls)
        create_operations(cls, cls.stock)


#TODO Rever os testes para simplificacao. Como agora nao existe mais operation
#sozinha temos que rever a organizacao do teste.
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
                                          'date': datetime.now(),
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
        self.assertEqual(str(response.data['operation_limit']), '30.8795813')

class BuyDataTest(OperationTestCase):
    def test_validation_buy(self):
        url = reverse('buy-list')
        response = self.client.post(url, {'stock': self.stock.pk,
                                          'date': datetime.now(),
                                          'amount': '200000',
                                          'price': '1000',
                                          'target': '40.00'})

        self.assertEqual(response.status_code, status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE)
