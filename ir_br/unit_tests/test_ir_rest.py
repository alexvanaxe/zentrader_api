from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse

from account.unit_tests.account_mocks import create_account
from stock.unit_tests.stock_mocks import create_stocks
from operation.unit_tests.operation_mocks import create_day_trades, create_ir_operations, create_operations


class IrBrTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        create_account(cls)
        create_stocks(cls)
        create_operations(cls, cls.stock)
        create_ir_operations(cls, cls.stock2)
        create_day_trades(cls, cls.stock2)

class IrBrTest(IrBrTestCase):
    def test_get(self):
        """ Test the simple get """
        url = reverse('ir_br')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_get_date(self):
        """ Test the simple get """
        url = reverse('ir_br_date', kwargs={'date': '2017-06-30T15:52:30' })
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data["ir"]), "2589.58")
        self.assertEqual(str(response.data["ir_daytrade"]), "3195.32")

