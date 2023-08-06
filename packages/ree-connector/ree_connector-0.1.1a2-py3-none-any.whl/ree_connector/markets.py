# MIT License

# Copyright (c) 2021 Jorge Marín

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Contributors:
#     Jorge Marín - initial Package version
"""
markets module
"""

from typing import Callable, List

from ree_connector.objects import Price
from ree_connector.utils import DocumentManager


class PvpcMarket:
    """
    This is a class for retrieve information of a determinated market session based on the date.

    Raises:
        ValueError: Throwed if value for location is not 'PEN' or 'CAN' case-insensitive

    Attributes:
        date (str): The market date you want to instantiate, format:'dd-mm-yyyy'.
        api_token (str): Authorized token to access REE-ESIOS API.
        location (str): Selector 'pen' or 'can' for work with prices for
        Iberian Peninsula and Balearic Islands or Canary Islands and Melilla.
    """

    def __init__(self, date:str, api_token:str, location:str) -> None:
        """
        The constructor for PvpcMarket class.

        Parameters:
           date (str): The market date you want to instantiate, format:'dd-mm-yyyy'.
           api_token (str): Authorized token to access REE-ESIOS API.
           location (str): Selector 'pen' or 'can' for work with prices for
           Iberian Peninsula and Balearic Islands or Canary Islands and Melilla.
        """
        self.__pvpc_url = (
            "http://api.esios.ree.es/archives/70/download_json?locale=es&date="
        )
        # self.doc_manager = DocumentManager(api_token)
        self.__location = location.lower()

        if not self.__location in ("pen", "can"):
            raise ValueError(
                "Only 'PEN(Iberian peninsula and Balearic Islands),\
                CAN(Canary Islands and Melilla)' values are allowed"
            )

        if self.__location == "pen":
            self.__price_location_lambda: Callable[
                [Price], float
            ] = lambda x: x.get_pen_price()
        elif self.__location == "can":
            self.__price_location_lambda: Callable[
                [Price], float
            ] = lambda x: x.get_can_price()

        self.json_object = DocumentManager(api_token).get_json_document(f"{self.__pvpc_url}{date}")
        self.__prices = [
            Price(interval["Hora"], date, interval["PCB"], interval["CYM"])
            for interval in self.json_object["PVPC"]
        ]

    def get_n_cheapest_hours(self, n_hours:int) -> List[Price]:
        """
        The function to get the n cheapests prices of the market session.

        Parameters:
            n_hours (int): The number of cheapests intervals to retrieve.

        Returns:
            list[Price]: A list containing the n cheapests prices.
        """
        cheapests = self.__prices
        _empty = [cheap.set_cheap(False) for cheap in cheapests]
        cheapests.sort(key=self.__price_location_lambda)
        cheapests = cheapests[: n_hours if n_hours <= 24 else 24]
        _empty = [cheap.set_cheap(True) for cheap in cheapests]
        return cheapests

    def get_session_min_price(self) -> Price:
        """
        The function get the cheapest price of the session.

        Returns:
            Price: A Price object.
        """
        return min(self.__prices, key=self.__price_location_lambda)

    def get_session_max_price(self) -> Price:
        """
        The function get the most expensive price of the session.

        Returns:
            Price: A Price object.
        """
        return max(self.__prices, key=self.__price_location_lambda)

    def get_session_prices(self)-> List[Price]:
        """
        The function to get all session prices.

        Returns:
            list[Price]: A list containing all session prices.
        """
        return self.__prices

    def get_pen_data_plot(self) -> List[tuple]:
        """
        The function to get Iberian Peninsula and Balearic Islands
        price ordered by hour

        Returns:
            List[tuple]: A list of tuples (hour,price) ordered by hour
        """
        return [(price.get_raw_hour(),price.get_pen_price()) for price in self.__prices]

    def get_can_data_plot(self) -> List[tuple]:
        """
        Iberian Peninsula and Balearic Islands or Canary Islands and Melilla

        Returns:
            List[tuple]: A list of tuples (hour,price) ordered by hour
        """
        return [(price.get_raw_hour(),price.get_can_price()) for price in self.__prices]
