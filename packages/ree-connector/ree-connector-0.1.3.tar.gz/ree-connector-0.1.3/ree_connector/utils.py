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
Module utils, includes Document manager class
"""
import json
import requests

from requests import RequestException

class DocumentManager:
    """
    Class to manage data retrieval from REE API.
    """
    def __init__(self, api_token) -> None:
        """
        Constructor of the DocumentManager class.

        Args:
            api_token (str): Access token key for access to API.
        """
        self.__api_token = api_token

    def get_json_document(self,endpoint) -> dict:
        """
        The function to get json documents from REE API.

        Args:
            endpoint (str): The url of the endpoint.

        Returns:
            dict: A dictionary containing all session info.
        """
        return self.__download_json(endpoint)

    def reload_api_key(self, api_token) -> None:
        """
        The function to reload api token.

        Args:
            api_token (str): Access token key for access to API.
        """
        self.__api_token = api_token

    def __download_json(self, endpoint) -> dict:
        """
        The function to get json documents from REE API.

        Args:
            endpoint (str): The url of the endpoint

        Returns:
            dict: A dictionary containing all session info.
        """
        header = {
            "Accept": "application/json; application/vnd.esios-api-v1+json",
            "Content-Type": "application/json",
            "Host": "api.esios.ree.es",
            "Authorization": f"Token token={self.__api_token}",
        }
        try:
            response = requests.request("GET", endpoint, headers=header, verify=True)
            resp = json.loads(response.text)
            return resp
        except RequestException as re_exc:
            return re_exc
