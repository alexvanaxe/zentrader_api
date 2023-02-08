from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse

from account.unit_tests.account_mocks import create_account
from stock.unit_tests.stock_mocks import create_stocks
from notes.unit_tests.notes_mocks import create_notes
from zen_oauth.unit_tests.user_mocks import create_test_user, create_auth
from operation.unit_tests.operation_mocks import create_operations

class NotesTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        create_test_user(cls)
        create_auth(cls, cls.user)
        create_account(cls)
        create_stocks(cls)
        create_operations(cls, cls.stock, cls.user)
        create_notes(cls, cls.operation)

class NoteTest(NotesTestCase):
    def test_get(self):
        """ Verify that returns two notes for the default exp operation """
        url = reverse('note-list')
        response = self.client.get(url, {'operation': self.operation.pk}, HTTP_AUTHORIZATION=self.auth)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(len(response.data)), '2')
        # self.assertEqual(response.data[0]["stock"]['code'], "XPTO3")


    def test_get_other_opr(self):
        """ Verify that returns no notes for the non default exp operation """
        url = reverse('note-list')
        response = self.client.get(url, {'operation': self.experience.pk}, HTTP_AUTHORIZATION=self.auth)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(len(response.data)), '0')
        # self.assertEqual(response.data[0]["stock"]['code'], "XPTO3")
