from django.test.testcases import TestCase
from django.core.cache import cache

from zen_oauth.unit_tests.user_mocks import create_test_user, create_auth
from account.unit_tests.account_mocks import create_account
from stock.unit_tests.stock_mocks import create_stocks
from experience.unit_tests.experience_mocks import create_exp_analysis
from trade_system.unit_tests.analysis_mock import update_analysis


class AnalysisModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cache.clear()
        create_test_user(cls)
        create_auth(cls, cls.user)
        create_account(cls)
        create_stocks(cls)
        create_exp_analysis(cls, cls.stock, cls.user)


class AnalysisModelTest(AnalysisModelTestCase):
    def test_grade(self):
        update_analysis(self, self.experience)
        self.assertEqual('25.00',
                         "{0:.2f}".format(self.experience.analysis.grade()))
        self.assertEqual("B", self.experience.analysis.grade_symbol())
