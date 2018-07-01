from stock.models import Stock


def create_stocks(cls):
    """
    Create some default stocks to be used in testing.
    :param cls:
    :return:
    """
    cls.stock = Stock.objects.create(code="XPTO3", price=20.00)
    cls.stock2 = Stock.objects.create(code="XPTO2", price=20.00)

