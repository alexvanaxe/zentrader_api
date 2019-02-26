from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse
from account.unit_tests.account_mocks import create_account, create_second_account
from zen_oauth.unit_tests.user_mocks import create_test_user, create_auth

class AccountTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        create_test_user(cls)
        create_auth(cls, cls.user)
        create_account(cls)
        create_second_account(cls)


class TestAccount(AccountTestCase):
    def test_list(self):
        """
        Test retrieve the list of all accounts
        """
        url = reverse('account-list')
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data[0]['operation_cost_position']), "15.00")
        self.assertEqual(str(len(response.data)), "1")
