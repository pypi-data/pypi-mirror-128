import os
import time
import numpy
import requests
from http import HTTPStatus
from predictor_api_client.common.exceptions import *
from predictor_api_client.common.logging import get_client_logger
from predictor_api_client.utils.data import DataWrapper
from predictor_api_client.utils.headers import (
    get_header_with_authentication_credentials,
    get_header_with_access_token,
    get_header_with_refresh_token
)


class PredictorApiClient(object):
    """Class implementing the lightweight client app for the Predictor API"""

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

    # Define the predicted data wrapper
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
        Initializes the PredictorApiClient.

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
        self.logger = get_client_logger(logging_configuration or PredictorApiClient.logging_configuration)

        # Set the basic attributes
        self.host = host if host else PredictorApiClient.host
        self.port = port if port else PredictorApiClient.port
        self.verify = verify if verify else PredictorApiClient.verify
        self.timeout = timeout if timeout else PredictorApiClient.timeout

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
        Signs-up a new user in the predictor API.

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
        Logs-in an existing user in the predictor API.

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
        Refreshes an access token in the predictor API.

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

    def predict(self, access_token, refresh_token, model_identifier, feature_values, feature_labels=None):
        """
        Calls .predict(...) on a predictor (model) via the API.

        :param access_token: access token
        :type access_token: str, optional
        :param refresh_token: refresh token
        :type refresh_token: str
        :param model_identifier: model identifier
        :type model_identifier: str
        :param feature_values: feature values
        :type feature_values: numpy.array
        :param feature_labels: feature labels, defaults to None
        :type feature_labels: list, optional
        :return: (data/error_info, status_code)
        :rtype: tuple
        """
        return self._predict(
            endpoint=self.predict_endpoint,
            access_token=access_token,
            refresh_token=refresh_token,
            model_identifier=model_identifier,
            feature_values=feature_values,
            feature_labels=feature_labels)

    def predict_proba(self, access_token, refresh_token, model_identifier, feature_values, feature_labels=None):
        """
        Calls .predict_proba(...) on a predictor (model) via the API.

        :param access_token: access token
        :type access_token: str, optional
        :param refresh_token: refresh token
        :type refresh_token: str
        :param model_identifier: model identifier
        :type model_identifier: str
        :param feature_values: feature values
        :type feature_values: numpy.array
        :param feature_labels: feature labels, defaults to None
        :type feature_labels: list, optional
        :return: (data/error_info, status_code)
        :rtype: tuple
        """
        return self._predict(
            endpoint=self.predict_proba_endpoint,
            access_token=access_token,
            refresh_token=refresh_token,
            model_identifier=model_identifier,
            feature_values=feature_values,
            feature_labels=feature_labels)

    def _predict(
            self,
            endpoint,
            access_token,
            refresh_token,
            model_identifier,
            feature_values,
            feature_labels=None):
        """
        Calls .<endpoint>(...) on a predictor (model) via the API.

        :param endpoint: endpoint to be called
        :type endpoint: method
        :param access_token: access token
        :type access_token: str
        :param refresh_token: refresh token
        :type refresh_token: str
        :param model_identifier: model identifier
        :type model_identifier: str
        :param feature_values: feature values
        :type feature_values: numpy.array
        :param feature_labels: feature labels, defaults to None
        :type feature_labels: list, optional
        :return: (data/error_info, status_code)
        :rtype: tuple
        """

        # Validate the input arguments
        if not model_identifier:
            raise NoModelIdentifierForPredictionError(f"Missing: <model_identifier>")
        if feature_values is None:
            raise NoFeatureValuesForPredictionError(f"Missing: <feature_values>")
        if not isinstance(model_identifier, str):
            raise UnsupportedModelIdentifierForPredictionError("Unsupported type: <model_identifier>")
        if not isinstance(feature_values, numpy.ndarray):
            raise UnsupportedFeatureValuesForPredictionError("Unsupported type: <feature_values>")
        if not isinstance(feature_labels, (list, tuple, type(None))):
            raise UnsupportedFeatureLabelsForPredictionError("Unsupported type: <feature_labels>")

        # Prepare the prediction data
        data = self._prepare_prediction_data(
            model_identifier=model_identifier,
            feature_values=feature_values,
            feature_labels=feature_labels)

        # Prepare the refresh token necessity flag
        needs_refresh = False

        # Predict the class(es)/probabilit(y/ies) using an identified model
        #
        # 1. call the prediction endpoint
        # 2. if access token refresh is required, refresh the access token
        # 3. if the access token got refreshed, re-call the prediction endpoint again

        # -------------------------------
        # 1. Call the prediction endpoint
        try:
            response = requests.post(
                url=endpoint,
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
                return self._prepare_prediction_response(data, response, endpoint)

        # ----------------------------------
        # 2. Handle the access token refresh
        if needs_refresh:
            response, status_code = self.refresh_access_token(refresh_token)
            if status_code != HTTPStatus.OK:
                return response, status_code

            # ----------------------------------
            # 3. Re-call the prediction endpoint
            response = requests.post(
                url=endpoint,
                json=data,
                headers=get_header_with_access_token(response.get("access_token")),
                verify=self.verify,
                timeout=self.timeout)
            return self._prepare_prediction_response(data, response, endpoint)

    # --------- #
    # Utilities #
    # --------- #

    def _prepare_prediction_data(self, model_identifier, feature_values, feature_labels=None):
        """
        Prepares the prediction data.

        :param model_identifier: model identifier
        :type model_identifier: str
        :param feature_values: feature values
        :type feature_values: numpy.array
        :param feature_labels: feature labels, defaults to None
        :type feature_labels: list, optional
        :return: predicted data
        :rtype: dict
        """

        # Prepare the feature values and labels
        feature_values = self.data_wrapper.wrap_data(feature_values)
        feature_labels = feature_labels if feature_labels else []

        # Return the prediction data
        return {
            "model": model_identifier,
            "features": {
                "values": feature_values,
                "labels": feature_labels,
            }
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

    def _prepare_prediction_response(self, data, response, endpoint):
        """
        Prepares the prediction response.

        :param data: data for prediction
        :type data: dict or str
        :param response: API response
        :type response: requests.Response
        :param endpoint: endpoint to be called
        :type endpoint: method
        :return: prepared response data
        :rtype: tuple
        """

        # Log the prediction
        self.logger.info(
            f"./{endpoint[(endpoint.rfind('/') + 1):]} ({response.status_code}) "
            f"data: {data}; "
            f"response: {response.json()}")

        # Return the prediction response
        if response.status_code == HTTPStatus.OK:
            return self.data_wrapper.unwrap_data(response.json().get("predicted")), response.status_code
        return response.json(), response.status_code

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
    def predict_endpoint(self):
        return f"{self.address}/predict"

    @property
    def predict_proba_endpoint(self):
        return f"{self.address}/predict_proba"

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
