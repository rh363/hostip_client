import re
from typing import Literal, Union
import requests

# Regular expression pattern for validating IPv4 addresses
IP_ADDRESS_PATTERN = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
IP_ADDRESS_REGEX = re.compile(IP_ADDRESS_PATTERN)

# Regular expression pattern for validating URLs
URL_PATTERN = r"^https?://[^\s/$.?#].[^\s]*$"
URL_REGEX = re.compile(URL_PATTERN)

# Default service URL for hostip.info
DEFAULT_SERVICE_URL = "https://api.hostip.info"

# Default format for response data, JSON or HTML
DEFAULT_FORMAT = "json"

# Placeholder for private IP address indication
PRIVATE_ADDRESS = "Private Address"


class InvalidIpAddress(Exception):
    """
    Exception raised for errors in the input IP address.
    This exception is used to indicate that a provided IP address
    is not valid according to expected format or criteria.
    """
    pass


class InvalidFormat(Exception):
    """
    Exception raised for errors in the input format.
    This exception is intended to be used when input data does
    not conform to the required formats.
    """
    pass


class InvalidServiceUrl(Exception):
    """
    Exception raised for errors in the service URL format.
    This exception is used to indicate that a given service URL is 
    not valid.
    """
    pass


class Client:
    # Properties to store geographic information
    country_name = None
    country_code = None
    city = None
    latitude = None
    longitude = None

    def __init__(self, ip_address: str, hostip_url=DEFAULT_SERVICE_URL,
                 use_format: Union[Literal["json"], Literal["html"]] = DEFAULT_FORMAT):
        """
        Initializes the Client with given IP address, service URL, and response format.
        
        Args:
            ip_address (str): The IP address to be validated and used in requests.
            hostip_url (str): The service URL to be validated and used for making requests.
            use_format (Literal["json", "html"]): The response format, either 'json' or 'html'.
        
        Raises:
            InvalidIpAddress: If the IP address does not match the valid pattern.
            InvalidServiceUrl: If the service URL does not match the valid pattern.
            InvalidFormat: If the format is not 'json' or 'html'.
        """
        # Validate IP address format
        ip_addresses = IP_ADDRESS_REGEX.findall(ip_address)
        if len(ip_addresses) != 1:
            raise InvalidIpAddress("invalid ip address format")

        # Validate service URL format
        if not URL_REGEX.match(hostip_url):
            raise InvalidServiceUrl(f"invalid hostip url, may follow {DEFAULT_SERVICE_URL}")

        # Validate response format
        if not use_format in ["json", "html"]:
            raise InvalidFormat("invalid format, may be json or html")

        # Initialize instance variables
        self._format = use_format
        self._service_url = hostip_url
        self._ip_address = ip_addresses[0]

        # Formulate request URL
        url = f"{self._service_url}/get_{self._format}.php"

        # Make a request to the service with the given IP address
        response = requests.get(url, params={"ip": self._ip_address, "position": "true"})

        # Parse response based on the format requested
        if self._format == "json":
            self._data = response.json()
            self.country_name: str | None = self._data.get("country_name", None)
            if PRIVATE_ADDRESS in self.country_name:
                self.country_name = PRIVATE_ADDRESS
            self.country_code: str | None = self._data.get("country_code", None)
            self.city: str | None = self._data.get("city", None)
        else:
            self._data = response.text
            lines = self._data.split("\n")
            # Extract data from response lines assuming HTML format
            for line in lines:
                if "Country" in line:
                    country = line.split(":")[1].strip()
                    if PRIVATE_ADDRESS in country:
                        self.country_name = PRIVATE_ADDRESS
                        self.country_code = "XX"
                    else:
                        country_infos = country.split("(")
                        self.country_name = country_infos[0].strip()
                        self.country_code = country_infos[1].strip()[:-1]
                    continue
                if "City" in line:
                    self.city = line.split(":")[1].strip()
                    continue
                if "Latitude" in line:
                    self.latitude = line.split(":")[1].strip()
                    continue
                if "Longitude" in line:
                    self.longitude = line.split(":")[1].strip()
