from django.test.testcases import TestCase

from zen_fortune.models import Fortune


class FortuneGenericTests(TestCase):
    """
    TestCase containing generics tests of the fortune model.
    """
    def testAFortune(self):
        """ Instanciate a fortune and check if a message is there. """
        aFortune = Fortune()
        self.assertIsNotNone(aFortune.cookie)
