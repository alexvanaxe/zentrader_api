from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse
from stock.unit_tests.stock_mocks import create_stocks
from zen_oauth.unit_tests.user_mocks import create_test_user, create_auth


class StockTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        create_test_user(cls)
        create_auth(cls, cls.user)
        create_stocks(cls)


class TestStock(StockTestCase):
    def test_get(self):
        """
        Test the retrieve of a single stock
        """
        url = reverse('stock-detail', kwargs={'pk': self.stock.pk})
        response = self.client.get(url, HTTP_AUTHORIZATION=self.auth)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], "XPTO3")

    def test_patch(self):
        """
        Test the retrieve of a single stock
        """
        url = reverse('stock-detail', kwargs={'pk': self.stock.pk})
        response = self.client.patch(url, {'price': 34}, HTTP_AUTHORIZATION=self.auth)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['price'], "34.00")
