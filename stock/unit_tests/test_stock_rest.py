from rest_framework.test import APITestCase
from rest_framework import status

from django.core.urlresolvers import reverse
from stock.unit_tests.stock_mocks import create_stocks


class StockTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        create_stocks(cls)


class TestStock(StockTestCase):
    def test_get(self):
        """
        Test the retrieve of a single stock
        """
        url = reverse('stock-detail', kwargs={'pk': self.stock.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], "XPTO3")

    def test_put(self):
        """
        Test the retrieve of a single stock
        """
        url = reverse('stock-detail', kwargs={'pk': self.stock.pk})
        response = self.client.patch(url, {'price': 34})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['price'], "34.00")