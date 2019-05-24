
from django.test.testcases import TestCase
from django.core.cache import cache

from experience.models import ExperienceData
from stock.unit_tests.stock_mocks import create_stocks
from account.unit_tests.account_mocks import create_account
from operation.unit_tests.operation_mocks import create_operations
from zen_oauth.unit_tests.user_mocks import create_test_user, create_auth


class OperationModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cache.clear()
        create_test_user(cls)
        create_auth(cls, cls.user)
        create_account(cls)
        create_stocks(cls)


class ExperimentDataModelTest(OperationModelTestCase):
    def test_experiment_default(self):
        create_operations(self, self.stock, self.user)
        self.assertEqual('None', str(self.operation.target_gain_percent()))

    def test_total_percentage_experiment(self):
        create_operations(self, self.stock, self.user)
        experience = ExperienceData.objects.get(pk=self.operation.pk)
        self.assertEqual('-9.96', "{0:.2f}".format(experience.experience_total_gain_percent()))

    def test_target_percentage(self):
        create_operations(self, self.stock, self.user)
        experience = ExperienceData.objects.get(pk=self.operation.pk)
        self.assertEqual('30.02', "{0:.2f}".format(experience.operation_average_price()))

    def test_av_price(self):
        create_operations(self, self.stock, self.user)
        experience = ExperienceData.objects.get(pk=self.experience.pk)
        self.assertEqual('-33.39', "{0:.2f}".format(experience.target_gain_percent()))
