# GeoIP Client Package

This package provides a client for accessing geographic information about an IP address using the hostip.info API. It validates IP addresses and URLs, and handles JSON and HTML response formats.

## Features

- Validate IPv4 addresses and service URLs.
- Retrieve geographic information such as country name, country code, city, latitude, and longitude using hostip.info API.
- Handle responses in both JSON and HTML formats.

## Installation

To install the package, clone the repository and install the necessary dependencies:

```bash
pip install hostip-client==1.0.2
```

## Usage

### Import the Client

```python
from hostip_client.client import Client
```

### Create a Client Instance

To create an instance of the `Client`, provide a valid IP address, service URL, and an optional format (either 'json' or 'html').

```python
ip_address = "8.8.8.8"  # Replace with a valid IP address
client = Client(ip_address=ip_address)
```

### Handling Exceptions

- `InvalidIpAddress`: Raised when the provided IP address is not in a valid format.
- `InvalidServiceUrl`: Raised when the service URL is not valid.
- `InvalidFormat`: Raised if the format is not 'json' or 'html'.

### Accessing Geographic Information

Once a `Client` instance is created, access the geographic information like so:

```python
print("Country Name:", client.country_name)
print("Country Code:", client.country_code)
print("City:", client.city)
print("Latitude:", client.latitude)
print("Longitude:", client.longitude)
```

## Configuration

- **Service URL:** You can specify a different hostip.info service endpoint by passing a custom URL to `hostip_url`.
- **Format:** Choose either `json` or `html` format by setting the `use_format` property during initialization.

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss further.

## Acknowledgments

This package uses the [hostip.info](https://www.hostip.info) API for geographic data.