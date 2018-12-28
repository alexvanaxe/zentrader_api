from rest_framework.test import APITestCase

from django.urls import reverse
from rest_framework import status

import account.unit_tests.account_mocks as account_mocks
import stock.unit_tests.stock_mocks as stock_mocks
import learning.unit_tests.learning_mocks as learning_mocks

class LearningTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        account_mocks.create_account(cls)
        stock_mocks.create_stocks(cls)
        learning_mocks.create_paper_buy_sell(cls, cls.stock)

class LearningPaperBuyTest(LearningTestCase):
    def test_post(self):
        url = reverse('paper_buy-list')

        response = self.client.post(url, {'stock': self.stock.pk,
                                          'amount': '20000',
                                          'price': '10',
                                          'target': '15.00'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get(self):
         url = reverse('paper_buy-detail', kwargs={'pk': self.paper_buy.pk})

         response = self.client.get(url)

         self.assertEqual(response.status_code, status.HTTP_200_OK)
         self.assertEqual(response.data['amount'], "1000")


class LearningPaperSellTest(LearningTestCase):
    def test_post(self):
        url = reverse('paper_sell-list')

        response = self.client.post(url, {'stock': self.stock.pk,
                                          'paper_buy': self.paper_buy.pk,
                                          'amount': '20000',
                                          'price': '10',
                                          'target': '15.00'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get(self):
         url = reverse('paper_sell-detail', kwargs={'pk': self.paper_sell.pk})

         response = self.client.get(url)

         self.assertEqual(response.status_code, status.HTTP_200_OK)
         self.assertEqual(response.data['price'], "34.00")
