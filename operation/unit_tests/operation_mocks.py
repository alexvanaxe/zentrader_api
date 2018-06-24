from datetime import datetime

from operation.models import ExperienceData
from account.models import Account


def create_operations(cls, stock):
    cls.operation = ExperienceData.objects.create(stock=stock,
                                                  account=Account.objects.all()[0],
                                                  date=datetime.strptime('2017-06-30T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                  amount=1000, price=30)

    cls.operation_archived = ExperienceData.objects.create(stock=stock,
                                                           account=Account.objects.all()[0],
                                                           date=datetime.strptime('2017-06-30T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           amount=1000, price=20,
                                                           archived=True)

    cls.experience = ExperienceData.objects.create(stock=stock,
                                                   account=Account.objects.all()[0],
                                                   date=datetime.strptime('2017-06-30T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                   target=20, stop_loss=28,
                                                   amount=1000, price=30)

    cls.experience_archived = ExperienceData.objects.create(stock=stock,
                                                            account=Account.objects.all()[0],
                                                            date=datetime.strptime('2017-06-30T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                            amount=1000, price=20,
                                                            archived=True, stop_loss=20)
