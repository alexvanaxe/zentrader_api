""" An utility module, with the purpose of calculate and work with information regarding the Brazilian IR

    TODO: Existem potenciais problemas e questoes:
    * No calculo apenas consideramos vendas.
    * O que acontece quando uma compra eh daytrade?
"""
from collections import OrderedDict
from datetime import datetime
from decimal import Decimal, ROUND_DOWN
from operation.models import SellData

from formulas import support_system_formulas


def _separate_sell(sell, separated_sells, separated_daytrade):
    try:
        if sell.category == 'DT':
            separated_daytrade[(sell.creation_date.month, sell.creation_date.year)].append(sell)
        else:
            separated_sells[(sell.creation_date.month, sell.creation_date.year)].append(sell)
    except KeyError:
        if sell.category == 'DT':
            separated_daytrade[(sell.creation_date.month, sell.creation_date.year)] = [sell]
        else:
            separated_sells[(sell.creation_date.month, sell.creation_date.year)] = [sell]
    return (separated_sells, separated_daytrade)


def _iter_sells(sell_operations, index, separated_sells, separated_daytrade):
    if (len(sell_operations) > index):
        (separated_sells, separated_daytrade) = _separate_sell(sell_operations[index], separated_sells, separated_daytrade)
        _iter_sells(sell_operations, index + 1, separated_sells, separated_daytrade)

    return (separated_sells, separated_daytrade)

def _calculate_sum_month(sells):
    return sum((sell.result() for sell in sells)), sum((sell.cost() for sell in sells)), sells[0].creation_date

def _calculate_sum_months(separated_sells):
    return (_calculate_sum_month(sells) for sells in separated_sells)

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
    separated_daytrade = OrderedDict()

    return _iter_sells(sell_operations, 0, separated_sells, separated_daytrade)

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
    return (_calculate_sum_months(separated_sells[0].values()), _calculate_sum_months(separated_sells[1].values()))

def calculate_negative_balance(results):
    """
    Calculate how much can be discounted in the month

    See the reference in the docs of how the ir is calculated. And in the provided url.

    Basically it gets a list of sell operations and calculates if there is a negative value to discount.

    .. warning:: This method was projected to get a list of sell_operations in a chronological order.

    .. seealso:: `Bussola do investidor <http://blog.bussoladoinvestidor.com.br/imposto-de-renda-em-acoes/>`_

    """
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

def calculate_ir_base_value(reference_date=None):
    """
    Calculates the base value where the tax will be taken.

    According to the actually used brazilian law, if the total sells of the month were inferior to 20000,
      this month don't need to be paid.


    Keyword Arguments:

    :param reference_date: reference_date: The reference date where the impost will be taken.


    .. seealso:: `Bussola do investidor <http://blog.bussoladoinvestidor.com.br/imposto-de-renda-em-acoes/>`_

    """
    # SEE: bussola do investidor, http://blog.bussoladoinvestidor.com.br/imposto-de-renda-em-acoes/
    if reference_date is None:
        reference_date = datetime.today()
    sell_operations = SellData.executions.filter(creation_date__lte=datetime.strptime('%d-%d-01' %
                                                                 (reference_date.year,
                                                                  reference_date.month),
                                                                 '%Y-%m-%d')).order_by('creation_date')
    negative_balance = calculate_negative_balance(calculate_results(sell_operations)[0])
    negative_balance_dt = calculate_negative_balance(calculate_results(sell_operations)[1])
    # Excludes the sells of the previous months, since the logic here is to get the ir per month
    sell_operation_query = SellData.executions.filter(creation_date__lte=reference_date).exclude(creation_date__lte=datetime.strptime('%d-%d-01' % (reference_date.year, reference_date.month), '%Y-%m-%d'))
    results = calculate_results(sell_operation_query)[0]
    results_dt = calculate_results(sell_operation_query)[1]


    # Process the daytrade value
    try:
        result_dt = next(results_dt)

        value_to_pay_dt = result_dt[0] + negative_balance_dt
    except StopIteration:
        value_to_pay_dt = Decimal(0)

    # Process the normal ir to pay
    try:
        result = next(results)

        if result[1] <= 20000:
            value_to_pay = Decimal(0)
        else:
            value_to_pay = result[0] + negative_balance
    except StopIteration:
        value_to_pay = Decimal(0)

    return (value_to_pay.quantize(Decimal('.05'), rounding=ROUND_DOWN), value_to_pay_dt.quantize(Decimal('.05')))

def calculate_impost_to_pay(reference_date=None):
    """
    Calculates the amount money that will be have to be paid in the ir.

    .. seealso:: `Bussola do investidor <http://blog.bussoladoinvestidor.com.br/imposto-de-renda-em-acoes/>`_

    Keyword Arguments:

    :param reference_date: The reference date from where the impost will be calculated.

    """
    if reference_date is None:
        reference_date = datetime.today()
    ir = calculate_ir_base_value(reference_date)[0]
    ir_dt = calculate_ir_base_value(reference_date)[1]

    return (support_system_formulas.calculate_ir(ir).quantize(Decimal('.05'), rounding=ROUND_DOWN), support_system_formulas.calculate_ir_daytrade(ir_dt).quantize(Decimal('.05'), rounding=ROUND_DOWN))


class IrBr():
    def __init__(self, ir, ir_daytrade):
        self.ir = ir
        self.ir_daytrade = ir_daytrade


class IrBrManager():
    def retrieveIr(self, reference_date=None):
        if reference_date is None:
            reference_date = datetime.today()
        ir_to_pay = calculate_impost_to_pay(reference_date)
        return IrBr(ir_to_pay[0], ir_to_pay[1])

