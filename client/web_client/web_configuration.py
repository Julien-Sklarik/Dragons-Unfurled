import os

import psycopg2.extras 
from utils.singleton import Singleton


class WebConfiguration(metaclass=Singleton):
    """
    Technical class to open only one connection to the DB.
    """

    def __init__(self):
        # Open the connection.
        self._api_url = os.environ["API_URL"]

    @property
    def connection(self):
        """
        return the opened connection.

        :return: the opened connection.
        """
        return self.__connection