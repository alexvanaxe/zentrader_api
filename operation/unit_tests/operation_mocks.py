from datetime import datetime

from operation.models import Operation, ExperienceData


def create_operations(cls, stock):
    cls.operation = ExperienceData.objects.create(stock=stock,
                                                  date=datetime.strptime('2017-06-30T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                  amount=1000, price=30)

    cls.operation_archived = ExperienceData.objects.create(stock=stock,
                                                           date=datetime.strptime('2017-06-30T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           amount=1000, price=20,
                                                           archived=True)

    cls.experience = ExperienceData.objects.create(stock=stock,
                                                   date=datetime.strptime('2017-06-30T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                   target=20, stop_loss=28,
                                                   amount=1000, price=30)

    cls.experience_archived = ExperienceData.objects.create(stock=stock,
                                                            date=datetime.strptime('2017-06-30T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                            amount=1000, price=20,
                                                            archived=True, stop_loss=20)
