from datetime import datetime

from experience.models import ExperienceData
from account.models import Account

def create_experiences(cls, stock, user):
    """
    Creates some basic experiences on the test database
    """
    cls.operation = ExperienceData.objects.create(stock=stock,
                                                  owner=user,
                                                  account=Account.objects.all()[0],
                                                  creation_date=datetime.strptime('2017-06-30T15:52:30',
                                                                                  '%Y-%m-%dT%H:%M:%S'),
                                                  amount=1000,
                                                  price=30)

    cls.operation_archived = ExperienceData.objects.create(stock=stock, owner=user,
                                                           account=Account.objects.all()[0],
                                                           creation_date=datetime.strptime('2017-06-30T15:52:30',
                                                                                           '%Y-%m-%dT%H:%M:%S'),
                                                           amount=1000, price=20,
                                                           archived=True)

    cls.experience = ExperienceData.objects.create(stock=stock, owner=user,
                                                   account=Account.objects.all()[0],
                                                   creation_date=datetime.strptime('2017-06-30T15:52:30',
                                                                                   '%Y-%m-%dT%H:%M:%S'),
                                                   target=20, stop_loss=28,
                                                   amount=1000, price=30)

    cls.experience_archived = ExperienceData.objects.create(stock=stock, owner=user,
                                                            account=Account.objects.all()[0],
                                                            creation_date=datetime.strptime('2017-06-30T15:52:30',
                                                                                            '%Y-%m-%dT%H:%M:%S'),
                                                            amount=1000, price=20,
                                                            archived=True)

def create_exp_analysis(cls, stock, user):
    cls.experience = ExperienceData.objects.create(stock=stock, owner=user,
                                                   account=Account.objects.all()[0],
                                                   creation_date=datetime.strptime('2017-06-30T15:52:30',
                                                                                   '%Y-%m-%dT%H:%M:%S'),
                                                   target=84, stop_loss=28,
                                                   amount=1, price=80)

