# Featurizer API client

![GitHub last commit](https://img.shields.io/github/last-commit/BDALab/featurizer-api-client)
![GitHub issues](https://img.shields.io/github/issues/BDALab/featurizer-api-client)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/BDALab/featurizer-api-client)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/featurizer-api-client)
![GitHub top language](https://img.shields.io/github/languages/top/BDALab/featurizer-api-client)
![PyPI - License](https://img.shields.io/pypi/l/featurizer-api-client)

This package provides a [PyPi-installable](https://pypi.org/project/featurizer-api-client/) lightweight client application for the [Featurizer API](https://github.com/BDALab/featurizer-api/) RESTFull server application. The package implements `FeaturizerApiClient` class enabling fast and easy method-based calls to all endpoints accessible on the API. To make working with the client a piece of cake, it provides full-documented example scripts for each of the supported endpoints. For more information about the Featurizer API, please read the official [readme](https://github.com/BDALab/featurizer-api#readme) and [documentation](https://github.com/BDALab/featurizer-api/tree/master/docs).

_The full programming sphinx-generated docs can be seen in the [official documentation](https://featurizer-api-client.readthedocs.io/en/latest/)_.

**Endpoints**:
1. featurization endpoints (`/featurize`)
    1. `/featurize` - calls `.extract` on the specified features-extractor (featurizer interface)
2. security endpoints (`/signup`, `/login`, and `/refresh`)
    1. `/signup` - signs-up a new user.
    2. `/login` - logs-in an existing user (obtains access and refresh authorization tokens).
    3. `/refresh` - refreshes an expired access token (obtains refreshed authorization access token).

**Contents**:
1. [Installation](#Installation)
2. [Configuration](#Configuration)
3. [Data](#Data)
4. [Examples](#Examples)
5. [License](#License)
6. [Contributors](#Contributors)

---

## Installation

```
pip install featurizer-api-client
```

## Configuration

The package provides the following configuration of the `FeaturizerApiClient` object during the instantiation:
1. API deployment specific configuration: it supports the configuration of the `host` (IP address), `port` (port number), and other settings related to the deployment and operation of the Featurizer API (for more information, see the `docs/`).
2. API client specific configuration: it supports the configuration of the logging (`logging_configuration`). In this version, the package provides logging of the successful as well as unsuccessful `/featurize` endpoint calls (for more information, see the `docs/`).

## Data

The full description of the requirements on input/output data (format, shape, etc.) can be found [here](https://github.com/BDALab/featurizer-api#data).

## Examples

In general, every time a client is used, the `FeaturizerApiClient` class must be instantiated. Next, all endpoint-specific data must be prepared. And finally, the endpoint-specific methods can be called. The full example scripts for each of the supported endpoints are placed at `./examples` (simplified examples are shown bellow).

### Client instantiation

```python
from pprint import pprint
from http import HTTPStatus
from featurizer_api_client import FeaturizerApiClient

# Prepare the featurizer API client settings
#
# ---------------------------------------------- #
# Must be same as for the running Featurizer API #
# ---------------------------------------------- #
#
# 1. host (IP address)
# 2. port (port number)
# 3. request verification
# 4. request timeout in seconds
host = "http://127.0.0.1"
port = 5000
verify = True
timeout = 2

# Instantiate the featurizer API client
client = FeaturizerApiClient(host=host, port=port, verify=verify, timeout=timeout)
```

### User sign-up

```python
# This example assumes the presence of the client instantiation code

# TODO: prepare data for a new user (see the API's requirements on the password)
#
# 1. username
# 2. password (e.g. can be generated with https://passwordsgenerator.net/)
username = "<TODO: FILL-IN>"
password = "<TODO: FILL-IN>"

print("\n-- [01] example --")
print(f"Signing-up a new user with username: {username} and password: {password}\n")

# Sign-up a new user
response, status_code = client.sign_up(username, password)

# Check the output
if status_code == HTTPStatus.OK:
    print("Successfully signed-up a new user")
else:
    print(f"The request was unsuccessful ({status_code}): {response}")

print("Response:")
pprint(response)
```

### User log-in

```python
# This example assumes the presence of the client instantiation code

# TODO: prepare data for an existing user (data from: user sign-up)
#
# 1. username
# 2. password
username = "<TODO: FILL-IN>"
password = "<TODO: FILL-IN>"

print("\n-- [02] example --")
print(f"Logging-in an existing user with username: {username} and password: {password}\n")

# Log-in an existing user
response, status_code = client.log_in(username, password)

# Check the output
if status_code == HTTPStatus.OK:
    print("Successfully logged-in an existing user")
else:
    print(f"The request was unsuccessful ({status_code}): {response}")

print("Response:")
pprint(response)
```

### Expired access token refresh

```python
# This example assumes the presence of the client instantiation code

# TODO: prepare data for request authorization (refresh token from: user log-in)
refresh_token = "<TODO: FILL-IN>"

print("\n-- [03] example --")
print("Refreshing an expired access token\n")

# Refresh an expired access token
response, status_code = client.refresh_access_token(refresh_token)

# Check the output
if status_code == HTTPStatus.OK:
    print("Successfully refreshed an expired access token")
else:
    print(f"The request was unsuccessful ({status_code}): {response}")

print("Response:")
pprint(response)
```

### Featurization

```python
# This example assumes the presence of the client instantiation code

import numpy

# TODO: prepare data for request authorization (access token and refresh token)
access_token = "<TODO: FILL-IN>"
refresh_token = ">TODO: FILL-IN>"

# TODO: prepare pipeline of features
#
# Example:
# features_pipeline = [
#     {
#         "name": "feature 1",
#         "args": {"abc": 123, "def": 456}
#     },
#     {
#         "name": "feature 2",
#         "args": {"ghi": "simple", "jkl": False}
#     },
#     {
#         "name": "feature 3",
#         "args": {}
#     }
# ]
features_pipeline = "<TODO: FILL-IN>"

# TODO: prepare feature extractor configuration
extractor_configuration = "<TODO: FILL-IN>"

# TODO: prepare featurizer data (sample values/labels)
#
# ----------------------------------------------------- #
# Must meet the data requirements of the Featurizer API #
# ----------------------------------------------------- #
#
# Example (10 subjects, each having 100 1-D samples):
# sample_values = numpy.random.rand(10, 1, 100)
# sample_labels = None
sample_values = "<TODO: FILL-IN>"
sample_labels = None

print("\n-- [04] example --")
print(f"Calling .featurize(...) on a feature extractor\n")

# Call .featurize(...) on a feature extractor
response, status_code = client.featurize(
    features_pipeline=features_pipeline,
    sample_values=sample_values,
    sample_labels=sample_labels,
    extractor_configuration=extractor_configuration,
    access_token=access_token,
    refresh_token=refresh_token)

# Check the output
if status_code == HTTPStatus.OK:
    print("Successfully called .featurize(...)")
else:
    print(f"The request was unsuccessful ({status_code}): {response}")

print("Response:")
pprint(response)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributors

This package is developed by the members of [Brain Diseases Analysis Laboratory](http://bdalab.utko.feec.vutbr.cz/). For more information, please contact the head of the laboratory Jiri Mekyska <mekyska@vut.cz> or the main developer: Zoltan Galaz <galaz@vut.cz>.