from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse
from account.unit_tests.account_mocks import create_account

class AccountTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        create_account(cls)


class TestAccount(AccountTestCase):
    def test_list(self):
        """
        Test retrieve the list of all accounts
        """
        url = reverse('account-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['broker'], "test")
