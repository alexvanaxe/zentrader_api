from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse

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

    def test_patch(self):
        """ Verify that a patch update is possible. """
        url = reverse('experience-detail', kwargs={'pk': self.operation.pk})
        response = self.client.patch(url, {"amount": 200},
                                     HTTP_AUTHORIZATION=self.auth)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['amount'], "200")

    def test_get(self):
        """ Verify that everything is correct in the configuration """
        url = reverse('experience-list')
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(len(response.data)), '2')
        # self.assertEqual(response.data[0]["stock"]['code'], "XPTO3")

    def get_archived(self):
        """ Verify that the application doesnt return the archived opperations """
        url = reverse('experience-list')
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data[0]["price"]), "30.00")

    def test_delete(self):
        """ Verify that a delete is possible. """
        url = reverse('experience-detail', kwargs={'pk': self.operation.pk})
        response = self.client.delete(url, HTTP_AUTHORIZATION=self.auth)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ExperienceDataTest(OperationTestCase):
    def test_post(self):
        url = reverse('experience-list')
        response = self.client.post(url, {'stock': self.stock.pk,
                                          'amount': '200',
                                          'price': '10',
                                          'target': '40.00'}, HTTP_AUTHORIZATION=self.auth)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_archived(self):
        url = reverse('experience-list')
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(len(response.data)), '2')

    def patch_nested(self):
        """ Test if the patch is possible with a nested operation """
        url = reverse('experience-detail', kwargs={'pk': self.experience.pk})
        response = self.client.patch(url, {'stop_gain': 36}, HTTP_AUTHORIZATION=self.auth)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data['stop_gain']), '36.00')

    def test_gain(self):
        url = reverse('experience-detail', kwargs={'pk': self.experience.pk})
        response = self.client.get(url + '?detailed=true', HTTP_AUTHORIZATION=self.auth)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data['target_gain']), '-10020.01')

    def test_gain2(self):
        url = reverse('experience-detail', kwargs={'pk': self.experience.pk})
        response = self.client.get(url + '?detailed=true', HTTP_AUTHORIZATION=self.auth)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual("{0:.2f}".format(response.data['operation_limit']), '31.00')
