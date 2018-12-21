"""
Holder of the formulas in the system

To be adherent to the DRY principle, all the mathematical formulas are to be concentrated in this module, as the
 methods that performs the calculations itself.
"""

import parser
from decimal import Decimal, ROUND_DOWN

# Imposts and taxes constants
EMOLUMENTOS=Decimal(0.0050)
LIQUIDACAO=Decimal(0.0275)
IR_PERCENTAGE=Decimal(15)
IR_DT_PERCENTAGE=Decimal(20)
PIRANHA_LIMIT=Decimal(3)
SHARK_LIMIT=Decimal(10)

SIMPLE_PERCENTAGE = "(partial * 100) / total"

GRADE = "((gain * Decimal('100'))/((top - bottom) * Decimal('100')))"

OPERATION_PRICE = "Decimal(amount) * Decimal(value)"

TOTAL_MONEY = "equity + gain"

PIRANHA = "(stop_loss * 100) / total_money"

STOP_LOSS_PRICE = "(((value - stop_loss) * amount)) + (operation_cost * 2)"

LIMIT = "((piranha * total_money) - (Decimal(operation_cost) * Decimal(200)) + (stop_loss * amount * 100)) / (amount * 100)"

IR_FORMULA = "month * %s / 100" % IR_PERCENTAGE

IR_DT_FORMULA = "month * %s / 100" % IR_DT_PERCENTAGE

EMOLUMENTOS_FORMULA = "(Decimal(%s) * operation_price) / 100" % EMOLUMENTOS

LIQUIDACAO_FORMULA = "(Decimal(%s) * operation_price) / 100" % LIQUIDACAO

AVERAGE_PRICE = "(( %s ) + Decimal(operation_cost) + %s + %s)/Decimal(amount)" % (OPERATION_PRICE, EMOLUMENTOS_FORMULA, LIQUIDACAO_FORMULA)

SELL_TOTAL_COST="((value * amount) - operation_cost - (%s) - (%s))" % (EMOLUMENTOS_FORMULA, LIQUIDACAO_FORMULA)

BUY_TOTAL_COST = "(buy_value * amount + operation_cost)"

GAIN_PERCENT = "((total_gain) * 100)/(buy_value * amount + operation_cost)"

GAIN = "(((sell_value * amount) - operation_cost) - ((Decimal(%s) * sell_value) / 100) - ((Decimal(%s) * sell_value) / 100)) - (((avg_buy_value * amount + operation_cost)) + ((Decimal(%s) * avg_buy_value) / 100) + ((Decimal(%s) * avg_buy_value) / 100))" % (EMOLUMENTOS, LIQUIDACAO, EMOLUMENTOS, LIQUIDACAO)

AVERAGE_GAIN = "((sell_value * amount) - operation_cost - (%s) - (%s)) - (average_buy_price * amount)" % (EMOLUMENTOS_FORMULA, LIQUIDACAO_FORMULA)


def calculate_percentage(partial, total):
    """
    A simple generic function to calculate a percentage based on a partial from a total.
    """
    return eval(getParsedFormula(SIMPLE_PERCENTAGE))


def calculate_price(amount, value):
    """
    Applies the formula of the price of the operation.

    ::

     Formula: amount * value

    """
    return eval(getParsedFormula(OPERATION_PRICE))


def calculate_grade(gain, top, bottom):
    """
    Applies the formula of the grade of the trade.

    ::

     Formula: ((gain * Decimal('100'))/((top - bottom) * Decimal('100')))

    """
    try:
        return eval(getParsedFormula(GRADE))
    except TypeError:
        pass


def calculate_piranha(stop_loss, total_money):
    """
    Applies the formula of the piranha.

    ::

      Formula: (stop_loss * 100) / total_money

    """

    return eval(getParsedFormula(PIRANHA))


def calculate_total_money(equity, gain):
    """
    Applies the formula of the total money I have.

    ::

      Formula: equity + gain

    """
    return eval(getParsedFormula(TOTAL_MONEY))


def calculate_stop_loss_price(value, stop_loss, amount, operation_cost):
    """
    Applies the formula of the total price of the loss.

    ::

      Formula: (((value - stop_loss) * amount)) + (operation_cost * 2)

    """
    if not stop_loss:
        stop_loss = 0
    return eval(getParsedFormula(STOP_LOSS_PRICE))


def calculate_sell(amount, value, operation_cost):
    """
    Return the amount of money will be added to our account in a sell discounted the operation cost and taxes.
    """
    operation_price = eval(getParsedFormula(OPERATION_PRICE))

    return eval(getParsedFormula(SELL_TOTAL_COST))


def calculate_gain(sell_value, avg_buy_value, amount, operation_cost):
    """
    Applies the formula of the gain. It considers the emolumentos, liquidation
    for the buy and for the sell and the operation cost.

    ::

      Formula: (sell_value * amount - operation_cost - emulmentos - liquidacao) - (avg_buy_value * amount + emulmentos + liquidacao)

    """
    # value = buy_value
    # total_compra = eval(getParsedFormula(OPERATION_PRICE))
    # operation_price = Decimal(buy_value)
    # total_compra += eval(getParsedFormula(EMOLUMENTOS_FORMULA))
    # total_compra += eval(getParsedFormula(LIQUIDACAO_FORMULA))
    #
    # operation_price = Decimal(sell_value)
    # total_venda = eval(getParsedFormula(SELL_TOTAL_COST))
    # total_venda -= eval(getParsedFormula(EMOLUMENTOS_FORMULA))
    # total_venda -= eval(getParsedFormula(EMOLUMENTOS_FORMULA))

    return eval(getParsedFormula(GAIN))


def calculate_gain_percent(sell_value, buy_value, amount, operation_cost):
    """
    Applies the formula of the percentage gain.

    ::

      Formula: (((sell_value * amount - operation_cost) - (buy_value * amount + operation_cost)) * 100)/(buy_value * amount + operation_cost)

    """
    total_gain = calculate_gain(sell_value, buy_value,
                                amount, operation_cost)

    return eval(getParsedFormula(GAIN_PERCENT))


def calculate_limit(piranha, total_money, operation_cost, stop_loss, amount):
    """
    Applies the formula of the limit.

    ::

      Formula: ((piranha * total_money) - (Decimal(operation_cost) * Decimal(200)) + (stop_loss * amount * 100)) / (amount * 100)

    """
    return eval(getParsedFormula(LIMIT))


def calculate_average_price(amount, value, operation_cost):
    """
    Applies the formula of the average price.
    This formula is used on IR.

    ::

      Formula: ((amount * value) + operation_cost)/amount

    """
    operation_price = eval(getParsedFormula(OPERATION_PRICE))

    return eval(getParsedFormula(AVERAGE_PRICE))


def calculate_average_gain(sell_value, average_buy_price, operation_cost, amount):
    """
    Applies the formula of the average gain.

    This formula is used on IR.

    ::

      Formula: ((sell_value * amount) - operation_cost) - (average_buy_price * amount)

    """
    value = sell_value
    operation_price = eval(getParsedFormula(OPERATION_PRICE))

    return eval(getParsedFormula(AVERAGE_GAIN))


def calculate_ir(month):
    """
    Applies the formula of the ir.

    This formula is used on IR.

    ::

      Formula: month * 15 / 100

    """
    return eval(getParsedFormula(IR_FORMULA))


def calculate_ir_daytrade(month):
    """
    Applies the formula of the ir for the daytrade

    This formula is used on IR of the daytrade mode.

    ::

      Formula: month * 20 / 100

    """
    return eval(getParsedFormula(IR_DT_FORMULA))


def calculate_emolumentos(operation_price):
    """
    Calculates the cost of the emolumento

    ::

      Formula: "(EMOLUMENTOS% * 100) / operation_cost"

    """
    return eval(getParsedFormula(EMOLUMENTOS_FORMULA))


def calculate_liquidacao(operation_price):
    """
    Calculates the cost of the liquidacao

    ::

      Formula: "(LIQUIDACAO% * 100) / operation_cost"

    """
    return eval(getParsedFormula(LIQUIDACAO_FORMULA))


def getParsedFormula(formula):
    """
    Get the parsed formula to be processed.

    Arguments:

    :param formula: A formula that will be transformed into a code

    :return: Returns a code to be processed

    """
    code = parser.expr(formula).compile()
    return code


def calculate_grade_symbol(grade):
    """ Calculates the grade symbol """
    if grade is None:
        return None

    if grade < 10:
        return 'D'
    if 10 <= grade <= 20:
        return 'C'
    if 20 < grade <= 30:
        return 'B'
    if grade > 30:
        return 'A'
