""" An utility module, with the purpose of calculate and work with information regarding the Brazilian IR """
from collections import OrderedDict
from datetime import datetime
from decimal import Decimal, ROUND_DOWN
from operation.models import SellData

from formulas import support_system_formulas

def separate_months(sell_operations):
    """
    Separate the sells in months

    Given a list o SellDatas, this method process it and returns a dict with a tuble (mm, yyyy) as key
     and a list of sells as value.

    That way we can get all sells of any months easily for processing, without requiring to make queries for that.

    .. warning::  This method was projected to get a list of sell_operations in a chronological order.

    Arguments:

    :param sell_operations: A list of sell_operations. (See: control.models.SellData)

    """
    separated_sells = OrderedDict()

    def _separate_sell(sell, separated_sells):
        try:
            separated_sells[(sell.date.month, sell.date.year)].append(sell)
        except KeyError:
            separated_sells[(sell.date.month, sell.date.year)] = [sell]
        return separated_sells

    def _iter_sells(sell_operations, index, separated_sells):
        if (len(sell_operations) > index):
            separated_sells = _separate_sell(sell_operations[index], separated_sells)
            _iter_sells(sell_operations, index + 1, separated_sells)

        return separated_sells

    return _iter_sells(sell_operations, 0, separated_sells)


def calculate_results(sell_operations):
    """
    Returns a generator with a tuple like (balance, total money of sales) for each month that there was a sale

    The return will be a list like [(1000, 15000), (-500, 20000)...]

    It is used mostly to calculate the negative balance, and know if there is a discount in the ir to pay in the month.

    .. warning::  This method was projected to get a list of sell_operations in a chronological order.

    Arguments:
    :param sell_operations: A list of sell_operations. (See: control.models.SellData)

    """
    separated_sells = separate_months(sell_operations)

    def _calculate_sum_month(sells):
        return sum((sell.result() for sell in sells)), sum((sell.cost() for sell in sells)), sells[0].date

    def _calculate_sum_months(separated_sells):
        return (_calculate_sum_month(sells) for sells in separated_sells)

    return _calculate_sum_months(separated_sells.values())


def calculate_negative_balance(sell_operations):
    """
    Calculate how much can be discounted in the month

    See the reference in the docs of how the ir is calculated. And in the provided url.

    Basically it gets a list of sell operations and calculates if there is a negative value to discount.

    .. warning:: This method was projected to get a list of sell_operations in a chronological order.

    .. seealso:: `Bussola do investidor <http://blog.bussoladoinvestidor.com.br/imposto-de-renda-em-acoes/>`_

    """

    results = calculate_results(sell_operations)

    def _process_negative_balance(results, result, negative_balance):
        if result[0] < 0:
            negative_balance = result[0] + negative_balance
        elif result[1] > 20000:
            negative_balance = result[0] + negative_balance

        if negative_balance > 0:
            negative_balance = 0

        try:
            result = next(results)
            return _process_negative_balance(results, result, negative_balance)
        except StopIteration:
            pass

        return negative_balance
    try:
        return _process_negative_balance(results, next(results), 0)
    except StopIteration:
        return 0


def calculate_ir_base_value(reference_date=datetime.today()):
    """
    Calculates the base value where the tax will be taken.

    According to the actually used brazilian law, if the total sells of the month were inferior to 20000,
      this month don't need to be paid.


    Keyword Arguments:

    :param reference_date: reference_date: The reference date where the impost will be taken.


    .. seealso:: `Bussola do investidor <http://blog.bussoladoinvestidor.com.br/imposto-de-renda-em-acoes/>`_

    """
    # SEE: bussola do investidor, http://blog.bussoladoinvestidor.com.br/imposto-de-renda-em-acoes/
    sell_operations = SellData.objects.filter(date__lte=datetime.strptime('%d-%d-01' % (reference_date.year, reference_date.month), '%Y-%m-%d')).order_by('date')
    negative_balance = calculate_negative_balance(sell_operations)
    sell_operation_query = SellData.objects.filter(date__lte=reference_date).exclude(date__lte=datetime.strptime('%d-%d-01' % (reference_date.year, reference_date.month), '%Y-%m-%d'))
    results = calculate_results(sell_operation_query)
    try:
        result = next(results)
    except StopIteration:
        return Decimal(0)

    if result[1] <= 20000:
        return Decimal(0)
    else:
        value_to_pay = result[0] + negative_balance

    return value_to_pay.quantize(Decimal('.05'), rounding=ROUND_DOWN)


def calculate_impost_to_pay(reference_date=datetime.today()):
    """
    Calculates the amount money that will be have to be paid in the ir.

    .. seealso:: `Bussola do investidor <http://blog.bussoladoinvestidor.com.br/imposto-de-renda-em-acoes/>`_

    Keyword Arguments:

    :param reference_date: The reference date from where the impost will be calculated.

    """
    ir = calculate_ir_base_value(reference_date)

    return support_system_formulas.calculate_ir(ir).quantize(Decimal('.05'), rounding=ROUND_DOWN)
