"""Errors for the wrapper"""


class OCBaseException(Exception):
    """Base exception for all OC Transpo errors"""


class MissingKeyError(OCBaseException):
    """App ID and/or API Key was not provided"""


class APIException(OCBaseException):
    """Base exception for any error returned by the OC Transpo API"""


class InvalidKeyError(APIException):
    """Invalid API key or App ID"""


class QueryError(APIException):
    """Unable to query data source"""


class InvalidStopError(APIException):
    """Invalid stop number"""


class InvalidRouteError(APIException):
    """Invalid route number"""


class StopDoesntServiceError(APIException):
    """Stop does not service route at this time"""


class NoRoutesOnStopError(APIException):
    """No routes available at stop at any time"""


ERROR_CODES = {
    "1": InvalidKeyError,
    "2": QueryError,
    "10": InvalidStopError,
    "11": InvalidRouteError,
    "12": StopDoesntServiceError,
    "13": NoRoutesOnStopError,
}
