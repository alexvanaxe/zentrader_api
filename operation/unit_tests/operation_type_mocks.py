from operation.models import OperationType


def create_operation_types(cls):
    """
    Creates the default operation types
    :param cls:
    :return:
    """
    cls.operationType = OperationType.objects.create(name="experience")
    cls.operationTypeBuy = OperationType.objects.create(name="buy")
    cls.operationTypeSell = OperationType.objects.create(name="sell")
