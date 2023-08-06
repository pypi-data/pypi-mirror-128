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
Objects modules, includes Price class
"""
from datetime import datetime


class Price:
    """
    This is a class for instantiate a Price object.

    Attributes:
        __raw_hour (str): The session interval.
        __date (str): The session date.
        __pen_price (str): The price for Iberian Peninsula and Balearic Islands.
        __can_price (str): The price for Canary Island and Melilla.

    """

    def __init__(self, raw_hour: str, date: str, pen_price: str, can_price: str) -> None:
        """
        The constructor for Price class.

        Parameters:
            raw_hour (str): The session interval.
            date (str): The session date.
            pen_price (str): The price for Iberian Peninsula and Balearic Islands.
            can_price (str): The price for Canary Island and Melilla.
        """
        self.__raw_hour = raw_hour
        self.__date = date
        self.__pen_price = float(pen_price.replace(",", "."))
        self.__can_price = float(can_price.replace(",", "."))

        splitted_hour = self.__raw_hour.split("-")
        self.left_hour = datetime.now().replace(
            hour=int(splitted_hour[0] if splitted_hour[0] != "24" else "00"),
            minute=0,
            second=0,
        )
        self.right_hour = datetime.now().replace(
            hour=int(splitted_hour[1] if splitted_hour[1] != "24" else "00"),
            minute=0,
            second=0,
        )
        self._cheap = False
        self._under_avg = False

    def get_raw_hour(self) -> str:
        """
        The function to get the raw session interval.

        Returns:
            str: The session interval.
        """
        return self.__raw_hour

    def get_pen_price(self) -> float:
        """
        The function to get the price for Iberian Peninsula and Balearic Islands.

        Returns:
            str: The price for Iberian Peninsula and Balearic Islands.
        """
        return self.__pen_price

    def get_can_price(self) -> float:
        """
        The function to get the price for Canary Island and Melilla.

        Returns:
            str: The price for Canary Island and Melilla.
        """
        return self.__can_price

    def is_cheap(self):
        """
        The function to get the cheap value

        Returns:
            bool: True if is cheap price False if not
        """
        return self._cheap

    def set_cheap(self, is_cheap: bool):
        """
        Setter method to cheap attribute

        Args:
            is_cheap (bool): True or False
        """
        self._cheap = is_cheap

    def is_under_avg(self):
        """
        The function to get the under_avg value,
        indicates if the price is under the session average

        Returns:
            bool: True if is under_avg price False if not
        """
        return self._under_avg

    def set_under_avg(self, is_under_avg: bool):
        """
        Setter method to under_avg attribute

        Args:
            under_avg (bool): True or False
        """
        self._under_avg = is_under_avg

    def __repr__(self) -> str:
        """
        The function to represent Price object.

        Returns:
            str: The Price object formatted as a string.
        """
        return "('raw-hour':'%s','date':'%s','pen-price':'%.2f','can-price':'%.2f')" % (
            self.__raw_hour,
            self.__date,
            self.get_pen_price(),
            self.get_can_price(),
        )

    def __str__(self) -> str:
        """
        The function to print Price object.

        Returns:
            str: The Price object formatted as a string.
        """
        return "('raw-hour':'%s','date':'%s','pen-price':'%.2f','can-price':'%.2f')" % (
            self.__raw_hour,
            self.__date,
            self.get_pen_price(),
            self.get_can_price(),
        )
