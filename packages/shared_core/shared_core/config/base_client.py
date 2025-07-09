import json
from typing import Any, Dict, Optional

import requests

from ..utils import CentralizedLogger

# Initialize centralized logger for base_client
logger = CentralizedLogger.get_logger("base_client")


class BaseAPIClient:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        auth_type: str = "Bearer",
        basic_auth: Optional[str] = None,
        api_version: Optional[str] = None,
    ):
        """
        Initialize the API client

        Args:
            base_url (str): The base URL for the API
            api_key (str): The API key for authentication
            auth_type (str): The type of authentication (default: 'Bearer')
            basic_auth (str): The Basic auth string (if needed)
            api_version (str): API version to use in headers (if needed)
        """
        self.base_url = base_url
        self.api_key = api_key
        self.auth_type = auth_type
        self.basic_auth = basic_auth
        self.api_version = api_version

    def make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Make a request to the API

        Args:
            method (str): The HTTP method to use
            endpoint (str): The API endpoint
            data (dict, optional): The data to send in the request body
            params (dict, optional): The query parameters to include in the request

        Returns:
            dict: The JSON response from the API
        """
        url = f"{self.base_url}{endpoint}"

        headers = {
            "Content-Type": "application/json",
        }

        if self.auth_type == "Bearer":
            headers["Authorization"] = self.api_key
            # add API version if provided
            if self.api_version:
                headers["API-Version"] = self.api_version
        elif self.auth_type == "Basic":
            # use the basic_auth value if provided, otherwise fallback to api_key
            headers["Authorization"] = (
                f"Basic {self.basic_auth if self.basic_auth else self.api_key}"
            )
            # for D-Tools Cloud, also add the X-API-Key header
            headers["X-API-Key"] = self.api_key

        logger.debug(f"Making {method} request to {url}")
        logger.debug(f"Headers: {json.dumps(headers)}")
        if data:
            logger.debug(f"Data: {json.dumps(data)}")

        try:
            response = requests.request(
                method, url, json=data, params=params, headers=headers
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Request failed: {str(e)}")
            if "response" in locals():
                print(f"Response content: {response.text}")
            return {}
