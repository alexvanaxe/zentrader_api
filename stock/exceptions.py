"""
This is the module that contains the possible exceptions for the operation module to be returned
to the client.
"""
from rest_framework.exceptions import APIException
from rest_framework import status

class AutoUpdateStockError(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = 'Unable to update the stock. Call support!!'
    default_code = 'stock_error'
