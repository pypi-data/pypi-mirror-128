"""
Exceptions module.
"""
from yeelight import BulbException


class BulbConnectionLostException(BulbException):
    """ Raises when connection is lost """
