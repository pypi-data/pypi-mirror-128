import os
import time
import numpy
import requests
from http import HTTPStatus
from featurizer_api_client.common.exceptions import *
from featurizer_api_client.common.logging import get_client_logger
from featurizer_api_client.utils.data import DataWrapper
from featurizer_api_client.utils.headers import (
    get_header_with_authentication_credentials,
    get_header_with_access_token,
    get_header_with_refresh_token
)


class FeaturizerApiClient(object):
    """Class implementing the lightweight client app for the Featurizer API"""

    # Define the logging configuration
    logging_configuration = {
        "class": "logging.handlers.TimedRotatingFileHandler",
        "kwargs": {
            "when": "midnight",
            "interval": 1,
            "backupCount": 365,
            "encoding": "utf8",
            "filename": os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "..",
                "..",
                "logs",
                time.strftime("%Y_%m_%d_client.log")
            )
        }
    }

    # Define the featurized data wrapper
    data_wrapper = DataWrapper

    # Define the request attributes
    host = "http://127.0.0.1"
    port = 5000
    verify = True
    timeout = 2

    # Define the HTTP error codes to be handled by refreshing the access token
    refresh_required_errors = [
        HTTPStatus.UNAUTHORIZED,
        HTTPStatus.UNPROCESSABLE_ENTITY
    ]

    def __init__(self, host=None, port=None, verify=None, timeout=None, logging_configuration=None):
        """
        Initializes the FeaturizerApiClient.

        :param host: host (IP address), defaults to None
        :type host: str, optional
        :param port: port (port number), defaults to None
        :type port: str, optional
        :param verify: request verification, defaults to None
        :type verify: bool, optional
        :param timeout: timeout in seconds, defaults to None
        :type timeout: int. optional
        :param logging_configuration: logging configuration, defaults to None
        :type logging_configuration: dict, optional
        """

        # Set the client logger
        self.logger = get_client_logger(logging_configuration or FeaturizerApiClient.logging_configuration)

        # Set the basic attributes
        self.host = host if host else FeaturizerApiClient.host
        self.port = port if port else FeaturizerApiClient.port
        self.verify = verify if verify else FeaturizerApiClient.verify
        self.timeout = timeout if timeout else FeaturizerApiClient.timeout

        # Set the internal attributes
        self._username = None
        self._password = None
        self._access_token = None
        self._refresh_token = None

    # --------- #
    # Endpoints #
    # --------- #

    def sign_up(self, username, password):
        """
        Signs-up a new user in the featurizer API.

        :param username: username
        :type username: str
        :param password: password
        :type password: str
        :return: (data/error_info, status_code)
        :rtype: tuple
        """

        # Prepare the request body (username, password)
        body = get_header_with_authentication_credentials(username, password)

        # Sign-up a new user
        try:
            response = requests.post(url=self.signup_endpoint, json=body, verify=self.verify, timeout=self.timeout)
        except requests.ConnectionError:
            return {"message": "Connection error."}, HTTPStatus.NOT_FOUND
        else:
            return self._prepare_authentication_response(response)

    def log_in(self, username, password):
        """
        Logs-in an existing user in the featurizer API.

        :param username: username
        :type username: str
        :param password: password
        :type password: str
        :return: (data/error_info, status_code)
        :rtype: tuple
        """

        # Prepare the request body (username, password)
        body = get_header_with_authentication_credentials(username, password)

        # Log-in an existing user
        try:
            response = requests.post(url=self.login_endpoint, json=body, verify=self.verify, timeout=self.timeout)
        except requests.ConnectionError:
            return {"message": "Connection error."}, HTTPStatus.NOT_FOUND
        else:
            return self._prepare_authorization_response(response)

    def refresh_access_token(self, refresh_token):
        """
        Refreshes an access token in the featurizer API.

        :param refresh_token: refresh token
        :type refresh_token: str
        :return: (data/error_info, status_code)
        :rtype: tuple
        """

        # Prepare the request body (refresh token)
        body = get_header_with_refresh_token(refresh_token)

        # Refresh an access token
        try:
            response = requests.post(url=self.refresh_endpoint, headers=body, verify=self.verify, timeout=self.timeout)
        except requests.ConnectionError:
            return {"message": "Connection error."}, HTTPStatus.NOT_FOUND
        else:
            return self._prepare_authorization_response(response)

    def featurize(
            self,
            access_token,
            refresh_token,
            features_pipeline,
            sample_values,
            sample_labels=None,
            extractor_configuration=None):
        """
        Calls .featurize(...) on an injected featurization library via the API.

        :param access_token: access token
        :type access_token: str
        :param refresh_token: refresh token
        :type refresh_token: str
        :param features_pipeline: features pipeline
        :type features_pipeline: list of dicts
        :param sample_values: sample values
        :type sample_values: numpy.array
        :param sample_labels: sample labels, defaults to None
        :type sample_labels: list, optional
        :param extractor_configuration: extractor config, defaults to None
        :type extractor_configuration: dict, optional
        :return: (data/error_info, status_code)
        :rtype: tuple
        """

        # Validate the input arguments
        if not features_pipeline:
            raise NoFeaturesPipelineForFeaturizationError(f"Missing: <features_pipeline>")
        if sample_values is None:
            raise NoSampleValuesForFeaturizationError(f"Missing: <sample_values>")
        if not isinstance(features_pipeline, (list, tuple)):
            raise UnsupportedSampleValuesForFeaturizationError("Unsupported type: <features_pipeline>")
        if not isinstance(sample_values, numpy.ndarray):
            raise UnsupportedSampleValuesForFeaturizationError("Unsupported type: <sample_values>")
        if not isinstance(sample_labels, (list, tuple, type(None))):
            raise UnsupportedSampleLabelsForFeaturizationError("Unsupported type: <sample_labels>")

        # Prepare the featurization data
        data = self._prepare_featurization_data(
            features_pipeline=features_pipeline,
            sample_values=sample_values,
            sample_labels=sample_labels,
            extractor_configuration=extractor_configuration)

        # Prepare the refresh token necessity flag
        needs_refresh = False

        # Featurize the data using an injected featurization library
        #
        # 1. call the featurization endpoint
        # 2. if access token refresh is required, refresh the access token
        # 3. if the access token got refreshed, re-call the featurization endpoint again

        # ----------------------------------
        # 1. Call the featurization endpoint
        try:
            response = requests.post(
                url=self.featurize_endpoint,
                json=data,
                headers=get_header_with_access_token(access_token),
                verify=self.verify,
                timeout=self.timeout)
            if response.status_code in self.refresh_required_errors:
                needs_refresh = True

        except (requests.ConnectionError, requests.exceptions.ChunkedEncodingError):
            needs_refresh = True
        else:
            if not needs_refresh:
                return self._prepare_featurization_response(data, response)

        # ----------------------------------
        # 2. Handle the access token refresh
        if needs_refresh:
            response, status_code = self.refresh_access_token(refresh_token)
            if status_code != HTTPStatus.OK:
                return response, status_code

            # -------------------------------------
            # 3. Re-call the featurization endpoint
            response = requests.post(
                url=self.featurize_endpoint,
                json=data,
                headers=get_header_with_access_token(response.get("access_token")),
                verify=self.verify,
                timeout=self.timeout)
            return self._prepare_featurization_response(data, response)

    # --------- #
    # Utilities #
    # --------- #

    def _prepare_featurization_data(
            self,
            features_pipeline,
            sample_values,
            sample_labels=None,
            extractor_configuration=None):
        """
        Prepares the featurization data.

        :param features_pipeline: features pipeline
        :type features_pipeline: list of dicts
        :param sample_values: sample values
        :type sample_values: numpy.array
        :param sample_labels: sample labels
        :type sample_labels: list, optional
        :param extractor_configuration: feature extractor configuration
        :type extractor_configuration: dict, optional
        :return: featurization data
        :rtype: dict
        """

        # Prepare the sample values and labels
        sample_values = self.data_wrapper.wrap_data(sample_values)
        sample_labels = sample_labels if sample_labels else []

        # Prepare the extractor configuration
        extractor_configuration = extractor_configuration if extractor_configuration else {}

        # Return the featurization data
        return {
            "samples": {
                "values": sample_values,
                "labels": sample_labels,
            },
            "features": {
                "pipeline": features_pipeline
            },
            "extractor_configuration": extractor_configuration
        }

    def _prepare_authentication_response(self, response):
        """
        Prepares the authentication response.

        :param response: API response
        :type response: requests.Response
        :return: prepared response data
        :rtype: tuple
        """

        # Extract the authentication-data and status code
        data, state = response.json(), response.status_code

        # Call the authorization hooks
        self._update_username_hook(data.get("username"))
        self._update_password_hook(data.get("password"))

        # Return the authentication-data and status code
        return data, state

    def _prepare_authorization_response(self, response):
        """
        Prepares the authorization response.

        :param response: API response
        :type response: requests.Response
        :return: prepared response data
        :rtype: tuple
        """

        # Extract the authorization-data and status code
        data, state = response.json(), response.status_code

        # Call the authorization hooks
        self._update_access_token_hook(data.get("access_token"))
        self._update_refresh_token_hook(data.get("refresh_token"))

        # Return the authorization-data and status code
        return data, state

    def _prepare_featurization_response(self, data, response):
        """
        Prepares the featurization response.

        :param data: data for featurization
        :type data: dict or str
        :param response: API response
        :type response: requests.Response
        :return: prepared response data
        :rtype: tuple
        """

        # Log the featurization
        self.logger.info(f"./featurize ({response.status_code}) data: {data}; response: {response.json()}")

        # Prepare the featurization response
        if response.status_code == HTTPStatus.OK:
            features = response.json().get("features")
            features = {
                "values": self.data_wrapper.unwrap_data(features.get("values")),
                "labels": features.get("labels")
            }
        else:
            features = response.json()

        # Return the featurization response
        return features, response.status_code

    # ----- #
    # Hooks #
    # ----- #

    def _update_username_hook(self, username):
        self.username = username

    def _update_password_hook(self, password):
        self.password = password

    def _update_access_token_hook(self, access_token):
        self.access_token = access_token

    def _update_refresh_token_hook(self, refresh_token):
        self.refresh_token = refresh_token

    # ---------- #
    # Properties #
    # ---------- #

    @property
    def address(self):
        return f"{self.host}:{self.port}"

    @property
    def signup_endpoint(self):
        return f"{self.address}/signup"

    @property
    def login_endpoint(self):
        return f"{self.address}/login"

    @property
    def refresh_endpoint(self):
        return f"{self.address}/refresh"

    @property
    def featurize_endpoint(self):
        return f"{self.address}/featurize"

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        self._username = username

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, access_token):
        self._access_token = access_token

    @property
    def refresh_token(self):
        return self._refresh_token

    @refresh_token.setter
    def refresh_token(self, refresh_token):
        self._refresh_token = refresh_token
