"""
This is the module that contains the possible exceptions for the operation module to be returned
to the client.
"""
from rest_framework.exceptions import APIException
from rest_framework import status

class NotEnoughMoney(APIException):
    status_code = status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE
    default_detail = 'Not enough money to make this transaction'
    default_code = 'money_unavalable'


class NotEnoughStocks(APIException):
    status_code = status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE
    default_detail = 'Not enough stocks to make this transaction'
    default_code = 'stocks_unavalable'


class OperationExecuted(APIException):
    status_code = status.HTTP_423_LOCKED
    default_detail = 'This operation is already executed and can\'t be changed'
    default_code = 'operation_executed'


class NegativeStocksError(APIException):
    status_code = status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE
    default_detail = 'The amount of stocks negotiated has to be always greater than zero'
    default_code = 'negative_stocks'
