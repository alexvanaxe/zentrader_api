from datetime import datetime

from operation.models import Operation, ExperienceData


def create_operations(cls, stock, operationType):
    cls.operation = Operation.objects.create(stock=stock, operation_type=operationType,
                                             date=datetime.strptime('2017-06-30T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                             amount=1000, price=30)

    cls.operation_archived = Operation.objects.create(stock=stock, operation_type=operationType,
                                             date=datetime.strptime('2017-06-30T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                             amount=1000, price=20, archived=True)

    cls.experience = ExperienceData.objects.create(operation=cls.operation,
                                                   target=20, stop_loss=28)
    cls.experience_archived = ExperienceData.objects.create(operation=cls.operation_archived,
                                  stop_loss=20)
